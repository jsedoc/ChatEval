'''Processes the results from all of the HITs that have been run so far.'''

import glob
import os
import xmltodict
import argparse
import re
import codecs
import pickle
import scipy.stats
import numpy as np

import utils


parser = argparse.ArgumentParser(description='Analyzed the AMT HIT results for all of the provided HIT ids.')
parser.add_argument('-d', '--responses_path',
                    help='Path to a .pkl file containing HIT responses',
                    required=True)
parser.add_argument('-t','--target_list',
                    help='Text file containing paths to target files, one per line. These should be in the same order as they were when the HIT was launched.',
                    required=True)
parser.add_argument('-s', '--source_file',
                    required=True,
                    help="Source file, one source sentence per line.")
parser.add_argument('-b', '--sandbox',
                    default=False, action='store_true',
                    help='Set to true to run in the sandbox.')
                    
args = parser.parse_args()

def process_data(examples_dict):
  with open(args.responses_path, 'rb') as f_in:
    worker_results_list = pickle.load(f_in)

  for worker_results in worker_results_list:
    if worker_results['NumResults'] > 0:
      for assignment in worker_results['Assignments']:
        xml_doc = xmltodict.parse(assignment['Answer'])
        
        # This code assumes there are multiple fields in HIT layout
        for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
          input_field = answer_field['QuestionIdentifier']
          rank = int(answer_field['FreeText'])

          parsed = re.search(r'(ex-\d+)-target-(.+)', input_field)
          example_key = parsed.group(1)
          target_index_or_tie = parsed.group(2)
          
          example = examples_dict[example_key]
          if 'tie' in target_index_or_tie:
            example.votes.append(-1)
          else:
            target_index = int(target_index_or_tie)
            example.votes.append(target_index)

def print_vote_counts(examples_dict):
  l = [ex.votes for ex in examples_dict.values()]
  all_votes = [item for sublist in l for item in sublist]
  print('%d votes for 0' % sum([x == 0 for x in all_votes]))
  print('%d votes for 1' % sum([x == 1 for x in all_votes]))
  print('%d votes for -1' % sum([x == -1 for x in all_votes]))

  
def print_annotator_agreement(examples_dict):
  count_same = 0
  total = 0

  for ex in examples_dict.values():
    votes = ex.votes
    if len(votes) < 2:
      continue
    all_the_same = len(set(votes)) == 1
    if all_the_same:
      count_same += 1
    total += 1
  if total == 0:
    print('No examples have multiple votes')
  else:
    fraction = float(count_same) / total
    print('Of examples with >1 annotations, %f had 100%% agreement' % (fraction))

def print_distinct(examples_dict):
  tgt_0_responses = [ex.target_lines[0] for ex in examples_dict.values()]
  tgt_1_responses = [ex.target_lines[1] for ex in examples_dict.values()]

  distinct_1 = utils.distinct_1(tgt_0_responses)
  distinct_2 = utils.distinct_2(tgt_0_responses)
  print('Model 1 has scores:')
  print('distinct-1 = %f' % distinct_1)
  print('distinct-2 = %f' % distinct_2)

  distinct_1 = utils.distinct_1(tgt_1_responses)
  distinct_2 = utils.distinct_2(tgt_1_responses)
  print('Model 2 has scores:')
  print('distinct-1 = %f' % distinct_1)
  print('distinct-2 = %f' % distinct_2)

def print_t_test(examples_dict):
  means_0 = []
  means_1 = []

  for ex in examples_dict.values():
    votes = ex.votes

    # Ignore examples for which there is no vote data
    if len(votes) == 0:
      continue

    num_non_ties = len(list(filter(lambda x: x != -1, votes)))

    # Ignore examples for which all vote data says 'tie'
    if num_non_ties == 0:
      continue

    num_non_ties = float(num_non_ties)
    mean_response_0 = len(list(filter(lambda x: x == 0, votes))) / num_non_ties
    mean_response_1 = len(list(filter(lambda x: x == 1, votes))) / num_non_ties

    means_0.append(mean_response_0)
    means_1.append(mean_response_1)
  import pdb; pdb.set_trace()
  stat, pvalue = scipy.stats.ttest_ind(means_0, means_1, equal_var=True) 
  diff_in_means = np.mean(means_0) - np.mean(means_1)
  print('Difference between models is %f +/- %f (p=%f)' % (diff_in_means, stat, pvalue))

def print_num_annotators(examples_dict):
  counts = {}
  total_votes = 0
  for ex in examples_dict.values():
    num_votes = len(ex.votes)
    print(num_votes)
    if num_votes in counts:
      counts[num_votes] += 1
    else:
      counts[num_votes] = 1
    total_votes += len(ex.votes)
  for num_votes in counts.keys():
    print('%d examples have %d votes each.' % (counts[num_votes], num_votes))
  print('%s votes in total.' % (total_votes))


if __name__ == '__main__':
  # Read the examples into a dictionary 
  with open(args.target_list, 'r') as fin:
    target_files = fin.readlines()
    target_files = [x.strip() for x in target_files]
  examples = utils.process_source_and_responses(
      args.source_file, target_files)
  examples_dict = {}
  for example in examples:
    examples_dict[example.key] = example

  process_data(examples_dict)

  print_num_annotators(examples_dict)
  print()
  print_vote_counts(examples_dict) 
  print()
  print_annotator_agreement(examples_dict)
  print()
  print_distinct(examples_dict)
  print()
  print_t_test(examples_dict)

  # Check that the data looks reasonable.
  results_path = os.path.join(os.path.dirname(args.responses_path), 'results.txt')
  with codecs.open(results_path, 'w', encoding='utf-8') as fout:
    for example in examples:
      fout.write('\nSource: %s\n' % example.source_line.encode('utf-8').decode())
      for idx, line in enumerate(example.target_lines):
        fout.write('Candidate target: %s\n' % line.encode('utf-8').decode())
      fout.write('Winner is....: %s \n' % \
          ('It\'s a tie!' if len(example.votes) == 0 else str(example.votes)))

