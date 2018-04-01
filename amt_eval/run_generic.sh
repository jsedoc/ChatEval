source ~/venvs/mturk/bin/activate

ROOT=$PWD

S1=$1
S2=$2
SOURCE=$3

cd ~/Chatbot_evaluation/amt_eval/
python3.6 launch_2choice.py \
-n 10 \
-t "${ROOT}/${S1}" "${ROOT}/${S2}" \
-s "${ROOT}/${SOURCE}" \
-m 1 \

python3.6 launch_2choice.py \
-n 10 \
-t "${ROOT}/${S1}" "${ROOT}/${S2}" \
-s "${ROOT}/${SOURCE}" \
-m 1 \

python3.6 launch_2choice.py \
-n 10 \
-t "${ROOT}/${S1}" "${ROOT}/${S2}" \
-s "${ROOT}/${SOURCE}" \
-m 1 \

