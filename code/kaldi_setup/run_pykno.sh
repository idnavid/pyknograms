#! /usr/bin/python

pykno_dir=/erasable/nxs113020/ssc_pykno
. path.sh
. cmd.sh
trainsir=0dB
local/make_pykno.sh data/train_$trainsir $pykno_dir
#steps/compute_cmvn_stats.sh data/train_$trainsir exp/make_plp/train_$trainsir $plp_dir
steps/train_mono.sh  --nj 50 --cmd "$train_cmd" data/train_$trainsir data/lang exp/mono_pykno_$trainsir
utils/mkgraph.sh --mono data/lang exp/mono_pykno_$trainsir exp/mono_pykno_$trainsir/graph 


# Test:
testsir=clean
local/make_pykno.sh data/test_$testsir $pykno_dir
#steps/compute_cmvn_stats.sh data/test_$testsir exp/make_plp/test_$testsir $plp_dir


steps/decode.sh --nj 10 --cmd "$train_cmd" exp/mono_pykno_$trainsir/graph data/test_$testsir exp/mono_pykno_$trainsir/decode_toydev_$testsir

# Create hypothetic text sequency using decoding output (log files)
cat exp/mono_pykno_$trainsir/decode_toydev_$testsir/log/decode.* | grep "_" | grep -v "LOG" | grep -v "-" | sort > data/test_$testsir/text_pykno


