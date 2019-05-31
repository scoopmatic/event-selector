#!/bin/sh

# Prepare train and validation set
python gen_crf_feats.py $1 $2
crfsuite learn --set=c1=35.0 --set=c2=0.5 -m crf.model -e2 crf_train.tsv crf_val.tsv

# Prepare test set
python gen_crf_feats.py $1 $3
crfsuite/frontend/crfsuite tag -m crf.model -t -s label_bias=1:0.85 crf_val.tsv

crfsuite/frontend/crfsuite tag -m crf.model -s label_bias=1:0.85 crf_val.tsv > crf_val.pred
