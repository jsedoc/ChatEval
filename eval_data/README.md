# Evalution Datasets for Open Dialog Systems
## Neural Conversation Model
The 200 utterances used for evaluation in [A Neural Conversational Model](https://arxiv.org/abs/1506.05869) 
can be found in `neural_conv_model_eval_sources.txt`.
The responses from the model in the paper can be found in `neural_conv_model_eval_responses.txt`.
These were scraped from the [pdf](http://ai.stanford.edu/~quocle/QAresults.pdf) provided in the paper.

We provide responses from the following models.
* `neural_conv_model_eval_Responses.txt`: Responses from the original paper
* `neural_conv_model_cakechat_responses.txt`: Responses from the provided model checkpoint [here](https://github.com/lukalabs/cakechat)

## A Task of Dialogue System Technology Challenge 6
User-generated utterances  extracted from the dialogs used for evaluation in the [dbdc6 challenge](https://dbd-challenge.github.io/dbdc3/)
can be found in `dbdc_eval_minus_CIC_source.txt`. Conversations with the CIC bot
were omitted because they were more task-oriented than open domain. Random subsets of 200 utterances can
be found in `dbdc_eval_minus_CIC_source_200short.txt` and `dbdc_eval_minus_CIC_source_200long.txt`.
Short is 5 or fewer words. Long is 8 or more.

## Random Selection from Twitter and OpenSubtitles test sets
TODO

