''' Performs automatic evaluation on the provides model outputs '''

import glob
import os
import argparse
import codecs
import pickle
from gensim.models import KeyedVectors

import utils
import auto_eval_utils as aeu


# NOTE: sample runs file
# NCM,Cakechat,/home/jsedoc/Chatbot_evaluation/eval_data/ncm/neural_conv_model_eval_responses_cakechat.txt
# DBDC,OSQ,/data2/chatbot_eval_issues/results/AMT_DBDC_Test_OSC_OSQ/pred.txt.seed_701_no_emb_osq_acc_31.46_ppl_52.67_e13.pt

parser = argparse.ArgumentParser(description='Perform automatic evaluation.')
parser.add_argument('-r', '--runs_file',
                    help='File which has evaldataset, model, path as CSV with no header\n\t e.g. NCM,Cakechat,/home/jsedoc/Chatbot_evaluation/eval_data/ncm/neural_conv_model_eval_responses_cakechat.txt',
                    required=True)
parser.add_argument('-e', '--embedding_file',
                    help='Path to a word embedding file that can be processed by Gensim',
                    default='/data1/embeddings/eng/GoogleNews-vectors-negative300.bin',
                    required=False)
args = parser.parse_args()


if __name__ == '__main__':
  response_files = dict()
  response_files['NCM'] = dict()
  response_files['DBDC'] = dict()
  auto_eval = dict()
  auto_eval['NCM'] = dict()
  auto_eval['DBDC'] = dict()
  human_responses = dict()
  human_responses['NCM'] = {}
  human_responses['DBDC']={}

  for line in open(args.runs_file).readlines():
    evalset,model,response_file = line.strip('\n').split(',')
    # print(evalset,model,response_file)

    target_files = [response_file]
    print('Evaluation set is ' + evalset + ' model is: ' + model + ' response file: ' + response_file)
    response_files[evalset][model] = target_files[0]

    if evalset == 'NCM':
      examples = utils.process_source_and_responses(
        '/data2/chatbot_eval_issues/results/AMT_NCM_Test_NCM_Cakechat/neural_conv_model_eval_source.txt', target_files)
      human_responses['NCM']['Human1'] = [_.strip('\n') for _ in open('/home/jsedoc/Chatbot_evaluation/eval_data/ncm/neural_conv_model_eval_responses_human_1.txt').readlines()]
      human_responses['NCM']['Human2'] = [_.strip('\n') for _ in open('/home/jsedoc/Chatbot_evaluation/eval_data/ncm/neural_conv_model_eval_responses_human_2.txt').readlines()]
    elif evalset == 'DBDC':
      examples = utils.process_source_and_responses(
        '/data2/chatbot_eval_issues/results/AMT_DBDC_Test_OSQ_Harvard/dbdc_eval_minus_CIC_200rand.txt', target_files)
        
    examples_dict = {}
    for example in examples:
      examples_dict[example.key] = example

  binary_file = 'bin' in args.embedding_file
  w2v = KeyedVectors.load_word2vec_format(args.embedding_file, binary=binary_file)

  for evalset in response_files.keys():
    for model in response_files[evalset].keys():
      auto_eval[evalset][model] = dict()
      target_lines = [_.strip('\n') for _ in open(response_files[evalset][model]).readlines()]
      auto_eval[evalset][model]['Average Length'] = aeu.avg_len(target_lines)
      auto_eval[evalset][model]['distinct-1'] = aeu.distinct_1(target_lines)
      auto_eval[evalset][model]['distinct-2'] = aeu.distinct_2(target_lines)
      #auto_eval[evalset][model]['distinct-3'] = utils.distinct_3(target_lines)
      #auto_eval[evalset][model]['distinct-4'] = utils.distinct_4(target_lines)
      if evalset=='NCM':
        # NOTE: this will take both human references.
        auto_eval[evalset][model]['Average Sentence BLEU-2'] = aeu.bleu(target_lines, list(human_responses[evalset].values()))
        auto_eval[evalset][model]['Embedding Average Score'] = aeu.average_embedding_score(human_responses[evalset]['Human2'], target_lines, w2v)
        # NOTE: skipped.
        # embedding_metrics.greedy_match
        # embedding_metrics.extrema_score


        
import json            
print(json.dumps(auto_eval, sort_keys=True, indent=4, separators=(',', ': ')))


