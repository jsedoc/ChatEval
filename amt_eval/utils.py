import boto3
import codecs

class Example:
  '''Represents a single source line and all corresponding target lines
   we would like a Turker to evaluate.
  '''

  def __init__(self, source_line, key):
    self.source_line = source_line # The single source line
    self.target_lines = [] # List of all possible responses.
    self.key = key # This should be something short and unique.

    # for each target_line, contains a list of the ranking that line was assigned
    # This is not used for 2-choice evaluation
    self.ranks = []
    
    # This is used for 2-choice evaluation
    self.votes = []

  def add_target_line(self, target_line):
    self.target_lines.append(target_line)
    self.ranks.append([])

  def __str__(self):
    return "source='%s', targets='%s'" % (self.source_line, str(self.target_lines))


def process_source_and_responses(source_file, target_files):
  '''Read the source file and target files into a list of example objects.
  '''

  examples = []
  # with open(source_file, 'r') as s_f:
  with codecs.open(source_file, 'r', encoding="utf-8") as s_f:
    source_lines = s_f.readlines()
    for idx, line in enumerate(source_lines):
      example = Example(line.strip(), "ex-%03d" % (idx))
      examples.append(example)
    
  all_target_lines = []
  for target_file in target_files:
    # with open(target_file, 'r') as t_f:
    with codecs.open(target_file, 'r', encoding="utf-8") as t_f:
      target_lines_for_file = t_f.readlines()
      for idx, line in enumerate(target_lines_for_file):
        examples[idx].add_target_line(line.strip())

  return examples

def create_mturk_client(run_in_sandbox):
  '''Create the AMT client, which is used to post and read from HITs'''
  aws_access_key, aws_secret_access_key = read_keys_from_file()
  if run_in_sandbox:
    endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
  else:
    endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

  mturk = boto3.client(
      'mturk',
      aws_access_key_id=aws_access_key,
      aws_secret_access_key=aws_secret_access_key,
      region_name='us-east-1',
      endpoint_url = endpoint_url,
  )
  return mturk

def read_keys_from_file(filename='accessKeys.csv'):
  '''Readers Amazon credentials from the csv file that can be downloaded from Amazon'''

  with open(filename, 'r') as f:
    f.readline()
    aws_access_key, aws_secret_access_key = f.readline().strip().split(',')
  return aws_access_key, aws_secret_access_key

def distinct_1(lines):
  words = ' '.join(lines).split(' ')
  num_distinct_words = len(set(words))
  return float(num_distinct_words) / len(words)

def distinct_2(lines):
  all_bigrams = []
  num_words = 0

  for line in lines:
    line_list = line.split(' ')
    num_words += len(line_list)
    bigrams = zip(line_list, line_list[1:])
    all_bigrams.extend(list(bigrams))

  return len(set(all_bigrams)) / float(num_words)



