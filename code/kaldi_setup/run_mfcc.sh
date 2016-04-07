#! /usr/bin/bash

mfcc_dir=/erasable/nxs113020/ssc_mfcc


for sir in 0dB; do
echo "training channel: $channel"
steps/make_mfcc.sh --nj 200 --cmd "$train_cmd" data/train_$sir exp/make_mfcc/train_$sir $mfcc_dir
steps/compute_cmvn_stats.sh data/train_$sir exp/make_mfcc/train_$sir $mfcc_dir
#steps/train_mono.sh  --nj 50 --cmd "$train_cmd" data/train_$channel data/lang exp/mono_$channel
#utils/mkgraph.sh --mono data/lang exp/mono_$channel exp/mono_$channel/graph 
done;

