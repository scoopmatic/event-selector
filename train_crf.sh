#!/bin/sh

python gen_crf_feats.py
crfsuite learn -m crf.model -e2 crf_train.tsv crf_val.tsv
crfsuite/frontend/crfsuite tag -m crf.model -t -s label_bias=1:0.7 crf_val.tsv

crfsuite/frontend/crfsuite tag -m crf.model -s label_bias=1:0.7 crf_val.tsv > crf_val.pred
