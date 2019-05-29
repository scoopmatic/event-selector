#!/bin/sh

#python gen_crf_feats.py $1 $2

echo "_F1	MINFQ	STATE	TRANS	C1	C2	MEM	PERI	WEIGHT" > opt2.log
#echo "" > opt.log
for PERIOD in 10; do
  for MEM in 6; do
    for STATES in 0; do
      for TRANS in 0; do
        for MINFREQ in 0.0; do
          for C1 in 35 30 25 20; do
            for C2 in 0.0 0.1 0.25 0.5 1.0 2.5 5.0; do
              crfsuite learn --set=feature.minfreq=$MINFREQ --set=feature.possible_states=$STATES --set=feature.possible_transitions=$TRANS --set=c1=$C1 --set=c2=$C2 --set=num_memories=$MEM --set=period=$PERIOD -m crf.model -e2 crf_train.tsv crf_val.tsv
              for WEIGHT in 0.5 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95 1.0 1.1 1.2; do
                F1=$(crfsuite/frontend/crfsuite tag -m crf.model -t -s label_bias=1:$WEIGHT crf_val.tsv | grep "1: (" |cut -d" " -f11-|cut -b-6)
                echo "$F1\t$MINFREQ\t$STATES\t$TRANS\t$C1\t$C2\t$MEM\t$PERIOD\t$WEIGHT"
                echo "$F1\t$MINFREQ\t$STATES\t$TRANS\t$C1\t$C2\t$MEM\t$PERIOD\t$WEIGHT" >> opt2.log
              done;
            done;
          done;
        done;
      done;
    done;
  done;
done;




# 0.6297	0.0	0	0	1.0	0.7	12	20	1.2
