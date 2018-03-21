'''Processes the result from a HIT for diagnostics.'''

import xmltodict
import argparse

import utils

parser = argparse.ArgumentParser(description='Processes the AMT HIT results for all of the provided HIT ids.')
parser.add_argument('-d', '--hit_id',
                    help='A hit_id.',
                    required=True)
parser.add_argument('-b', '--sandbox',
                    default=False, action='store_true',
                    help='Set to true to run in the sandbox.')
args = parser.parse_args()

if __name__ == '__main__':
  mturk = utils.create_mturk_client(args.sandbox)

  worker_results = mturk.list_assignments_for_hit(
      HITId=args.hit_id, AssignmentStatuses=['Submitted'])
  if worker_results['NumResults'] > 0:
    for assignment in worker_results['Assignments']:
      xml_doc = xmltodict.parse(assignment['Answer'])
      
      print("Worker's answer was:")
      if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
        # Multiple fields in HIT layout
        for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
          print("For input field: " + answer_field['QuestionIdentifier'])
          print("Submitted answer: " + answer_field['FreeText'])
      else:
        # One field found in HIT layout
        print("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
        print("Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'])
  else:
    print("No results ready yet")
