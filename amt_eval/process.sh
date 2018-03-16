#!/bin/bash

source ~/py3.6env/bin/activate

ROOT=/data2/chatbot_eval_issues/results/AMT_Twitter_Test_Seed_1

if [ -e "${ROOT}/amt_hit_responses.pkl" ]
then
  echo "Accessing saved responses"
else
  echo 'Retrieving responses from AMT'
  python3.6 retrieve_responses.py \
  -d "${ROOT}/hits.txt" 
fi

python3.6 analyze_2choice_responses.py \
--target_list="${ROOT}/order.txt" \
--source_file="${ROOT}/twitter_test_prompt.txt" \
--responses_path="${ROOT}/amt_hit_responses.pkl" \
