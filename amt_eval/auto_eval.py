''' Performs automatic evaluation on the provides model outputs '''

import glob
import os
import argparse
import codecs
import pickle
import scipy.stats
import numpy as np
from gensim.models import KeyedVectors
from nltk.translate.bleu_score import sentence_bleu

import utils
import embedding_metrics

parser = argparse.ArgumentParser(description='Perform automatic evaluation.')
parser.add_argument('-t','--target_path',
                    help='Output utterances, one per line',
                    required=True)
parser.add_argument('-g', '--ground_truth_path',
                    help='Groundtruth output  utterances, one per line',
                    default=None)
parser.add_argument('-s', '--source_path',
                    required=True,
                    help="Input itternces, one per line. This can be a .TSV if there are multiple inputs.")
parser.add_argument('-e', '--embedding_path',
                    help='Path to a word embedding file that can be processed by Gensim',
                    required=True)
args = parser.parse_args()


def print_distinct(target_lines):

  distinct_1 = utils.distinct_1(target_lines)
  distinct_2 = utils.distinct_2(target_lines)
  print('Model 1 has scores:')
  print('distinct-1 = %f' % distinct_1)
  print('distinct-2 = %f' % distinct_2)


def print_bleu_scores(target_lines, gt_lines):
  avg_bleu = 0
  for (target_line, gt_line) in zip(target_lines, gt_lines):
    bleu = sentence_bleu(gt_line, target_line)
    avg_bleu += bleu
  avg_bleu = avg_bleu / len(target_lines)
  print('bleu = %d' % (avg_bleu))

def print_embedding_scores(target_lines, gt_lines, w2v):
  r = embedding_metrics.average(gt_lines, target_lines, w2v)
  print("Embedding Average Score: %f +/- %f ( %f )" %(r[0], r[1], r[2]))

  r = embedding_metrics.greedy_match(gt_lines, target_lines, w2v)
  print("Greedy Matching Score: %f +/- %f ( %f )" %(r[0], r[1], r[2]))

  r = embedding_metrics.extrema_score(gt_lines, target_lines, w2v)
  print("Extrema Score: %f +/- %f ( %f )" %(r[0], r[1], r[2]))

if __name__ == '__main__':
  if args.ground_truth_path is not None:
    with open(args.ground_truth_path, 'r') as f_gt:
      gt_lines = list(line.strip() for line in f_gt)
  else:
    gt_lines = None

  with open(args.source_path, 'r') as f_gt:
    source_lines = list(line.strip() for line in f_gt)

  with open(args.target_path, 'r') as f_gt:
    target_lines = list(line.strip() for line in f_gt)

  w2v = KeyedVectors.load_word2vec_format(
      args.embedding_path, binary=args.embedding_path.endswith(('bin')))

  # Make sure every file has the same number of lines.
  assert(len(source_lines) == len(target_lines))
  if gt_lines is not None:
    assert(len(source_lines) == len(gt_lines))

  print_distinct(target_lines)
  if source_lines is not None:
    print_embedding_scores(target_lines, gt_lines, w2v)
    print_bleu_scores(target_lines, gt_lines)
