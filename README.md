# Chatbot_evaluation
Chatbot evaluation is really hard. There is no standard, and this is our attempt to at least address small parts of this issue.

Right now we are attempting to use Parl AI as our framework http://parl.ai/. 

All of our checkpoints will be made publicly available including all configurations.

## ParlAI commands

I setup this way .... 
```
export PYTHONPATH=$PARLAI_PATH/ParlAI:$PARLAI_PATH/ParlAI/parlai
```

then to test via command prompt
```
 python3.6 examples/interactive.py -m seq2seq -mf /data2/chatbot_eval_issues/model_files/parlai/ncm_pc_replica_s2s_big -bs 1
 ```

to train

```
python3.6 examples/train_model.py -m seq2seq -e 50 -t personachat -dt train:stream -bs 32  -mf /data2/chatbot_eval_issues/model_files/parlai/ncm_pc_replica_s2s_big --gpu 2 -nl 2 -opt adagrad -lr 0.001 -hs 2048 -esz 2048 -tr 32
```

## OpenNMT commands
Data munging
```
python3.6 preprocess.py -train_src /data2/chatbot_eval_issues/datasets/MovieTriples/Shuffled_Subtle_Dataset.txt.train.A -train_tgt /data2/chatbot_eval_issues/datasets/MovieTriples/Shuffled_Subtle_Dataset.txt.train.B -valid_src /data2/chatbot_eval_issues/datasets/MovieTriples/Shuffled_Subtle_Dataset.txt.valid.A -valid_tgt /data2/chatbot_eval_issues/datasets/MovieTriples/Shuffled_Subtle_Dataset.txt.valid.B  -save_data data/subtle -share_vocab -src_words_min_frequency 1 -tgt_words_min_frequency 1 -src_vocab_size 100000 -tgt_vocab_size 100000 -max_shard_size 50000000
```

Standard training
```
python3.6 train.py -save_model seed_700_no_emb_subtle -seed 700 -data data/subtle -encoder_type brnn -global_attention mlp -word_vec_size 300 -rnn_size 512 -gpuid 2
```

to train with word embeddings
```

./tools/embeddings_to_torch.py -emb_file /data1/embeddings/eng/glove.42B.300d.txt -dict_file data/subtle.vocab.pt -output_file data/subtle_embeddings
python3.6 train.py  -seed 700 -save_model seed_700_glove_emb_subtle -data data/subtle -encoder_type brnn -global_attention mlp -word_vec_size 300 -rnn_size 512 -pre_word_vecs_enc data/subtle_embeddings.enc.pt -pre_word_vecs_dec data/subtle_embeddings.dec.pt -gpuid 0
```

trying out test data
```
python3.6 translate.py -model seed_700_no_emb_subtle_acc_26.75_ppl_63.93_e2.pt -src /data2/chatbot_eval_issues/datasets/MovieTriples/Validation_Shuffled_Dataset.txt.A -output pred.txt -replace_unk -verbose
```
