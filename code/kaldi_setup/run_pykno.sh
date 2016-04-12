#! /usr/bin/python

pykno_dir=/erasable/nxs113020/ssc_pykno
. path.sh
. cmd.sh


trainsir=0dB
. ~/.bashrc
#python local/pykno_feat_extraction.py data/train_$trainsir $pykno_dir
#~/bin/myJsplit -M 300 -b 1 -n pykno_ssc pykno_jobs.txt
#rm pykno_jobs.txt
#
#cat data/train_$trainsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){$pykno_dir="/erasable/nxs113020/ssc_pykno/"; print "/export/tools/kaldi-trunk3/src/featbin/copy-feats ark,t:${pykno_dir}/$1 ark,scp:${pykno_dir}/$1.ark,${pykno_dir}/$1.scp\n"}' > ark2scp_jobs.txt
#~/bin/myJsplit -M 300 -b 1 -n pykno_ssc ark2scp_jobs.txt
#
#rm data/train_$trainsir/feats.scp
#cat data/train_$trainsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){print `cat /erasable/nxs113020/ssc_pykno/$1.scp`}' >> data/train_$trainsir/feats.scp
#paste -d ' ' data/train_$trainsir/utt2spk data/train_$trainsir/feats.scp | cut -d ' ' -f 1,4 > tmp
#mv tmp data/train_$trainsir/feats.scp 
#
##est-pca --dim=20 scp:data/train_$trainsir/feats.scp data/train_$trainsir/pca.mat
##transform-feats data/train_$trainsir/pca.mat scp:data/train_$trainsir/feats.scp ark,scp:data/train_$trainsir/feats.ark,data/train_$trainsir/feats_pca.scp
##mv data/train_$trainsir/feats_pca.scp data/train_$trainsir/feats.scp
#
#steps/compute_cmvn_stats.sh data/train_$trainsir exp/make_pykno/train_$trainsir $pykno_dir
#rm -rf exp/mono_pykno_$trainsir
#bash local/train_mono_pca.sh  --nj 50 --cmd "$train_cmd" data/train_$trainsir data/lang exp/mono_pykno_$trainsir
#utils/mkgraph.sh --mono data/lang exp/mono_pykno_$trainsir exp/mono_pykno_$trainsir/graph 



# Test:
testsir=m3dB
python local/pykno_feat_extraction.py data/test_$testsir $pykno_dir
~/bin/myJsplit -M 300 -b 1 -n pykno_ssc pykno_jobs.txt
rm pykno_jobs.txt

cat data/test_$testsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){$pykno_dir="/erasable/nxs113020/ssc_pykno/"; print "/export/tools/kaldi-trunk3/src/featbin/copy-feats ark,t:$pykno_dir/$1 ark,scp:$pykno_dir/$1.ark,$pykno_dir/$1.scp\n"}' > ark2scp_jobs.txt
~/bin/myJsplit -M 300 -b 1 -n pykno_ssc ark2scp_jobs.txt

rm data/test_$testsir/feats.scp
cat data/test_$testsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){print `cat /erasable/nxs113020/ssc_pykno/$1.scp`}' >> data/test_$testsir/feats.scp

#transform-feats data/train_$trainsir/pca.mat scp:data/test_$testsir/feats.scp ark,scp:data/test_$testsir/feats.ark,data/test_$testsir/feats_pca.scp
#mv data/test_$testsir/feats_pca.scp data/test_$testsir/feats.scp

steps/compute_cmvn_stats.sh data/test_$testsir exp/make_pykno/test_$testsir $pykno_dir
bash steps/decode.sh --nj 10 --cmd "$train_cmd" exp/mono_pykno_$trainsir/graph data/test_$testsir exp/mono_pykno_$trainsir/decode_toydev_$testsir

# Create hypothetic text sequency using decoding output (log files)
cat exp/mono_pykno_$trainsir/decode_toydev_$testsir/log/decode.* | grep "_" | grep -v "LOG" | grep -v "-" | sort > data/test_$testsir/text_pykno

python local/find_accuracy.py data/test_$testsir/text_pykno O
