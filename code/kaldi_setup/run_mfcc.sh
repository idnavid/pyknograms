#! /usr/bin/bash

mfcc_dir=/erasable/nxs113020/ssc_mfcc
. path.sh
. cmd.sh
trainsir=0dB
#steps/make_mfcc.sh --nj 200 --cmd "$train_cmd" data/train_$sir exp/make_mfcc/train_$sir $mfcc_dir
#steps/compute_cmvn_stats.sh data/train_$sir exp/make_mfcc/train_$sir $mfcc_dir
#steps/train_mono.sh  --nj 50 --cmd "$train_cmd" data/train_$trainsir data/lang exp/mono_$trainsir
#utils/mkgraph.sh --mono data/lang exp/mono_$trainsir exp/mono_$trainsir/graph 


# Test:
testsir=0dB
#steps/make_mfcc.sh --nj 15 --cmd "$train_cmd" data/test_$testsir exp/make_mfcc/test_$testsir $mfcc_dir
#steps/compute_cmvn_stats.sh data/test_$testsir exp/make_mfcc/test_$testsir $mfcc_dir


steps/decode.sh --nj 10 --cmd "$train_cmd" exp/mono_$trainsir/graph data/test_$testsir exp/mono_$trainsir/decode_toydev_$testsir

# Create hypothetic text sequency using decoding output (log files)
cat exp/mono_$trainsir/decode_toydev_$testsir/log/decode.* | grep "_" | grep -v "LOG" | grep -v "-" | sort > data/test_$testsir/text


