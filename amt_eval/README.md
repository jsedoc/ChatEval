==Launch instructions for 2-choice experiment

```
source ~/py3.6env/bin/activate

ROOT=/data2/chatbot_eval_issues/results/AMT_Twitter_1

python3.6 launch_2choice.py \
-n 10 \
-t "${ROOT}/pred.txt.seed_700_no_emb_twitter_acc_22.38_ppl_141.44_e11" "${ROOT}/pred.txt.seed_701_no_emb_twitter_acc_22.33_ppl_141.55_e11" \
-s "${ROOT}/twitter_test_prompt.txt" \
-m 2 \
-b
```





