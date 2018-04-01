#encoding: utf-8

'''Launches a HIT on Amazon Mechanic Turk for rank-based evaluation of chatbot models'''

import boto3
import argparse
import random
import codecs
import html

import utils
import html_gen

parser = argparse.ArgumentParser(description='Launches AMT HITs for ranking task.')
parser.add_argument('-n', '--n_examples_per_hit',
                    type=int,
                    default=10,
                    help='The number of examples to display in a HIT')
parser.add_argument('-t','--target_files',
                    nargs='+',
                    help='List of files with target responses, each file has one target sentence per line.',
                    required=True)
parser.add_argument('-s', '--source_file',
                    required=True,
                    help="Source file, one source sentence per line.")
parser.add_argument('-m', '--max_assignments',
                    type=int,
                    default=1,
                    help="Max number of assignments.")
parser.add_argument('-b', '--sandbox',
                    default=False, action='store_true',
                    help='Set to true to run in the sandbox.')

args = parser.parse_args()

def create_HIT(examples, hit_id):
  num_target_candidates =  len(examples[0].target_lines)

  # For each of the provided examples, generate the html that allows
  # Turker to specify ranking. Also count the total number of reuqired radio buttons.
  tables_html = ''
  num_required = 0
  for idx in range(len(examples)):
    html, num_radio_buttons =  html_gen.generate_ranking_tables_html(examples[idx])
    tables_html += html
    num_required += num_radio_buttons

  instructions = html_gen.generate_multuchoice_instructions()

  # Generate the full HTML for the hit. The tables html gets inserts in the right place.
  question_html_value = html_gen.generate_HIT_html(num_required, tables_html, instructions)

  with codecs.open('task.html', 'w', encoding='utf-8') as fout:
    fout.write(question_html_value)

  question_html_value = question_html_value.encode('ascii', 'xmlcharrefreplace').decode()

  try:
    # These parameters define the HIT that will be created
    # question is what we defined above
    # max_assignments is the # of unique Workers you're requesting
    # title, description, and keywords help Workers find your HIT
    # duration is the # of seconds Workers have to complete your HIT
    # reward is what Workers will be paid when you approve their work
    # Check out the documentation on CreateHIT for more details
    if args.sandbox == False:
      check = raw_input("You are about to launch into production. Are you sure? [y/N] ")
      if not check in ['Y','y','Yes','yes']:
        exit()

    response = mturk.create_hit(
            Question=question_html_value,
            MaxAssignments=1,
            Title="Evaluate a chatbot system.",
            Description="Rank the responses of a chatbot",
            Keywords="question, answer, chatbot, research, dialog, rank",
            AssignmentDurationInSeconds=180,
            LifetimeInSeconds=172800,
            Reward="0.10")
            # UniqueRequestToken=hit_id)
  except Exception as e:
    import pdb; pdb.set_trace()
    print('Problem creating HIT')
    print(e)
    exit(1)

  # The response included several fields that will be helpful later
  hit_type_id = response['HIT']['HITGroupId']
  hit_id = response['HIT']['HITId']
  print("Your HIT has been created. You can see it at: "),
  print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
  print("Your HIT ID is: {}".format(hit_id))

  return hit_id

if __name__ == '__main__':
  # Create your connection to MTurk
  mturk = utils.create_mturk_client(args.sandbox)

  # Delete all existing HITs
  # existing_hits = mturk.list_hits()
  # import pdb; pdb.set_trace()  
  # for hit in existing_hits['HITs']:
    # hit_id = hit['HITId']
    # print('Deleting HIT: %s' % (hit_id))
    # mturk.delete_hit(HITId=hit_id)

  examples = utils.process_source_and_responses(args.source_file, args.target_files)
  print('Read in %d examples, each with %d possible targets.' % (len(examples), len(examples[0].target_lines)))

  assert args.n_examples_per_hit <= len(examples)

  random.shuffle(examples)

  # NOTE: last check.
  if args.sandbox == False:
    check = input("You are about to launch into production. Are you sure? [y/N] ")
    if not check in ['Y','y','Yes','yes']:
      exit()

  # TODO: For each set of k examples, create d HITs, where k is the number of
  # examples shown in a hit, and d is the number of random permutations of those
  # k HITs that we want to show.
  count = 0
  hit_ids = []
  while count < len(examples):
    print('Creating HIT for examples %s through %s' % (count, count+args.n_examples_per_hit-1))
    for idx in range(args.max_assignments):
      hit_id = create_HIT(examples[count:count+args.n_examples_per_hit], hit_id="cb_eval_%d_%d" % (count, idx))
      count+=10
      hit_ids.append(hit_id)

  # Write all the hit_ids to a file to make it easy to extact the results
  with open('hits.txt', 'w') as f_out:
    for hit_id in hit_ids:
      f_out.write('%s\n' % (hit_id))
