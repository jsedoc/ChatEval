import boto3
import codecs
import xmltodict
import re

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

    self.workers = []
    
    self.hits = []
    
    # This is used for 2-choice evaluation
    self.votes = []

  def source_line_utterances(self):
    '''The source line could actualy consist of multiple tab-separatted utterances.
      Retrive these as a list.
    '''
    return self.source_line.split('\t')

  def add_target_line(self, target_line):
    self.target_lines.append(target_line)
    self.ranks.append([])

  def __str__(self):
    return "source='%s', targets='%s', votes='%s'" % (self.source_line, str(self.target_lines), str(self.votes))


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

def process_amt_hit_responses(worker_results_list, examples_dict, invert=False):
  ''' Processes the worker_results_list and adds the vote information
      to each Example in the examples_dict
      If invert is True, set votes for first target to 1 and votes for 2nd target to 0
  '''

  for worker_results in worker_results_list:
    if worker_results['NumResults'] > 0:
      for assignment in worker_results['Assignments']:
        xml_doc = xmltodict.parse(assignment['Answer'])
        
        # This code assumes there are multiple fields in HIT layout
        for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
          if type(answer_field) == str:
            continue
          try:
            input_field = answer_field['QuestionIdentifier']
            rank = int(answer_field['FreeText'])
            worker_id = assignment['WorkerId']
            hit_id = assignment['HITId']
          except Exception as e:
            import pdb; pdb.set_trace()
            print(e)

          parsed = re.search(r'(ex-\d+)-target-(.+)', input_field)
          example_key = parsed.group(1)
          target_index_or_tie = parsed.group(2)
          
          example = examples_dict[example_key]
          if 'tie' in target_index_or_tie:
            example.votes.append(-1)
          else:
            target_index = int(target_index_or_tie)
            if invert:
              target_index = 0 if target_index == 1 else 0
            example.votes.append(target_index)
          example.workers.append(worker_id)
          example.hits.append(hit_id)
