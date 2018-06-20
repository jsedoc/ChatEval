from random import randint
from gensim.models import Word2Vec
import numpy as np


def distinct_1(lines):
  '''Computes the number of distinct words divided by the total number of words.

  Input:
  lines: List of strings.
  '''
  words = ' '.join(lines).split(' ')
  num_distinct_words = len(set(words))
  return float(num_distinct_words) / len(words)

def distinct_2(lines):
  '''Computes the number of distinct bigrams divided by the total number of words.

  Input:
  lines: List of strings.
  '''
  all_bigrams = []
  num_words = 0

  for line in lines:
    line_list = line.split(' ')
    num_words += len(line_list)
    bigrams = zip(line_list, line_list[1:])
    all_bigrams.extend(list(bigrams))

  return len(set(all_bigrams)) / float(num_words)

def avg_len(lines):
  '''Computes the average line length.

  Input:
  lines: List of strings.
  '''
  return(len([w for s in lines for w in s.strip().split()])/len(lines))

def bleu(target_lines, gt_lines, DEBUG=False):
  '''Computes the average BLEU score.
  
  Input:
  target_lines: List of lines produced by the model.
  gt_lines: List of ground-truth lines corresponding to each line produced by the model.
  '''

  # This import is in here because it is really slow, so only do it if we have to.
  from nltk.translate.bleu_score import sentence_bleu

  avg_bleu = 0
  num_refs = len(gt_lines)
  for i in range(len(target_lines)):
    ref = []
    for r in range(num_refs):
      ref.append(gt_lines[r][i].lower().split())
    hyp = target_lines[i].lower().split()
  
    bleu = sentence_bleu(ref, hyp, weights = (0.5, 0.5))
    if DEBUG == 2:
      print('CAND: ',target_lines[i])
      print('GT  : ',gt_lines[0][i])
      print('BLEU:', bleu)

    
    avg_bleu += bleu
  avg_bleu = avg_bleu / len(target_lines)
  return((avg_bleu))

"""
Everything below this comment was borrowed from https://github.com/julianser/hed-dlg-truncated/blob/master/Evaluation/embedding_metrics.py
(with some slight modifications)

Word embedding based evaluation metrics for dialogue.

This method implements three evaluation metrics based on Word2Vec word embeddings, which compare a target utterance with a model utterance:
1) Computing cosine-similarity between the mean word embeddings of the target utterance and of the model utterance
2) Computing greedy meatching between word embeddings of target utterance and model utterance (Rus et al., 2012)
3) Computing word embedding extrema scores (Forgues et al., 2014)

We believe that these metrics are suitable for evaluating dialogue systems.

Example run:

    python embedding_metrics.py path_to_ground_truth.txt path_to_predictions.txt path_to_embeddings.bin

The script assumes one example per line (e.g. one dialogue or one sentence per line), where line n in 'path_to_ground_truth.txt' matches that of line n in 'path_to_predictions.txt'.

NOTE: The metrics are not symmetric w.r.t. the input sequences. 
      Therefore, DO NOT swap the ground truths with the predicted responses.

References:

A Comparison of Greedy and Optimal Assessment of Natural Language Student Input Word Similarity Metrics Using Word to Word Similarity Metrics. Vasile Rus, Mihai Lintean. 2012. Proceedings of the Seventh Workshop on Building Educational Applications Using NLP, NAACL 2012.

Bootstrapping Dialog Systems with Word Embeddings. G. Forgues, J. Pineau, J. Larcheveque, R. Tremblay. 2014. Workshop on Modern Machine Learning and Natural Language Processing, NIPS 2014.


"""

def greedy_match(r1, r2, w2v):
  res1 = greedy_score(r1, r2, w2v)
  res2 = greedy_score(r2, r1, w2v)
  res_sum = (res1 + res2)/2.0

  return np.mean(res_sum), 1.96*np.std(res_sum)/float(len(res_sum)), np.std(res_sum)


def greedy_score(r1, r2, w2v):
  dim = w2v[w2v.index2word[0]].size  # embedding dimensions

  scores = []

  for i in range(len(r1)):
    tokens1 = r1[i].strip().split(" ")
    tokens2 = r2[i].strip().split(" ")
    X= np.zeros((dim,))
    y_count = 0
    x_count = 0
    o = 0.0
    Y = np.zeros((dim,1))
    for tok in tokens2:
      if tok in w2v:
        Y = np.hstack((Y,(w2v[tok].reshape((dim,1)))))
        y_count += 1

    for tok in tokens1:
      if tok in w2v:
        tmp  = w2v[tok].reshape((1,dim)).dot(Y)
        o += np.max(tmp)
        x_count += 1

    # if none of the words in response or ground truth have embeddings, count result as zero
    if x_count < 1 or y_count < 1:
      scores.append(0)
      continue

    o /= float(x_count)
    scores.append(o)

  return np.asarray(scores)


def extrema_score(r1, r2, w2v):
  scores = []

  for i in range(len(r1)):
    tokens1 = r1[i].strip().split(" ")
    tokens2 = r2[i].strip().split(" ")
    X= []
    for tok in tokens1:
      if tok in w2v:
        X.append(w2v[tok])
    Y = []
    for tok in tokens2:
      if tok in w2v:
        Y.append(w2v[tok])

    # if none of the words have embeddings in ground truth, skip
    if np.linalg.norm(X) < 0.00000000001:
      continue

    # if none of the words have embeddings in response, count result as zero
    if np.linalg.norm(Y) < 0.00000000001:
      scores.append(0)
      continue

    xmax = np.max(X, 0)  # get positive max
    xmin = np.min(X,0)  # get abs of min
    xtrema = []
    for i in range(len(xmax)):
      if np.abs(xmin[i]) > xmax[i]:
        xtrema.append(xmin[i])
      else:
        xtrema.append(xmax[i])
    X = np.array(xtrema)   # get extrema

    ymax = np.max(Y, 0)
    ymin = np.min(Y,0)
    ytrema = []
    for i in range(len(ymax)):
      if np.abs(ymin[i]) > ymax[i]:
        ytrema.append(ymin[i])
      else:
        ytrema.append(ymax[i])
    Y = np.array(ytrema)

    o = np.dot(X, Y.T)/np.linalg.norm(X)/np.linalg.norm(Y)

    scores.append(o)

  scores = np.asarray(scores)
  return np.mean(scores), 1.96*np.std(scores)/float(len(scores)), np.std(scores)


def average_embedding_score(r1, r2, w2v):
  dim = w2v[w2v.index2word[0]].size  # dimension of embeddings

  scores = []

  for i in range(len(r1)):
    tokens1 = r1[i].strip().split(" ")
    tokens2 = r2[i].strip().split(" ")
    X= np.zeros((dim,))
    for tok in tokens1:
      if tok in w2v:
        X+=w2v[tok]
    Y = np.zeros((dim,))
    for tok in tokens2:
      if tok in w2v:
        Y += w2v[tok]

    # if none of the words in ground truth have embeddings, skip
    if np.linalg.norm(X) < 0.00000000001:
      continue

    # if none of the words have embeddings in response, count result as zero
    if np.linalg.norm(Y) < 0.00000000001:
      scores.append(0)
      continue

    X = np.array(X)/np.linalg.norm(X)
    Y = np.array(Y)/np.linalg.norm(Y)
    o = np.dot(X, Y.T)/np.linalg.norm(X)/np.linalg.norm(Y)

    scores.append(o)

  scores = np.asarray(scores)
  return np.mean(scores), 1.96*np.std(scores)/float(len(scores)), np.std(scores)


