#!/bin/bash

source ~/venvs/mturk/bin/activate

ROOT=$PWD
SOURCE=$1

cd ~/Chatbot_evaluation/amt_eval/

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
--source_file="${ROOT}/${SOURCE}" \
--responses_path="${ROOT}/amt_hit_responses.pkl" \
