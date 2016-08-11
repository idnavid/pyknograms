#! /usr/bin/bash

. path.sh
. cmd.sh 

testsir=$1
run_mfcc() {
    mfcc_dir=ssc_mfcc
    trainsir=0dB
    #rm data/train_$trainsir/feats.scp
    #rm data/train_$trainsir/cmvn.scp
    #steps/make_mfcc.sh --nj 200 --cmd "$train_cmd" data/train_$trainsir exp/make_mfcc/train_$trainsir $mfcc_dir
    #steps/compute_cmvn_stats.sh data/train_$trainsir exp/make_mfcc/train_$trainsir $mfcc_dir
    #steps/train_mono.sh  --nj 50 --cmd "$train_cmd" data/train_$trainsir data/lang exp/mono_$trainsir
    #utils/mkgraph.sh --mono data/lang exp/mono_$trainsir exp/mono_$trainsir/graph 
    
    
    # Test:
    steps/make_mfcc.sh --nj 15 --cmd "$train_cmd" data/test_$testsir exp/make_mfcc/test_$testsir $mfcc_dir
    steps/compute_cmvn_stats.sh data/test_$testsir exp/make_mfcc/test_$testsir $mfcc_dir
    
    
    steps/decode.sh --nj 10 --cmd "$train_cmd" exp/mono_$trainsir/graph data/test_$testsir exp/mono_$trainsir/decode_toydev_$testsir
    
    # Create hypothetic text sequency using decoding output (log files)
    cat exp/mono_$trainsir/decode_toydev_$testsir/log/decode.* | grep "_" | grep -v "LOG" | grep -v "-" | sort > data/test_$testsir/text_mfcc
    
}
run_mfcc

run_plp() {
    plp_dir=ssc_plp
    trainsir=0dB
    #rm data/train_$trainsir/feats.scp
    #rm data/train_$trainsir/cmvn.scp
    #steps/make_plp.sh --nj 200 --cmd "$train_cmd" data/train_$trainsir exp/make_plp/train_$trainsir $plp_dir
    #steps/compute_cmvn_stats.sh data/train_$trainsir exp/make_plp/train_$trainsir $plp_dir
    #steps/train_mono.sh  --nj 50 --cmd "$train_cmd" data/train_$trainsir data/lang exp/mono_plp_$trainsir
    #utils/mkgraph.sh --mono data/lang exp/mono_plp_$trainsir exp/mono_plp_$trainsir/graph 
    
    
    # Test:
    steps/make_plp.sh --nj 15 --cmd "$train_cmd" data/test_$testsir exp/make_plp/test_$testsir $plp_dir
    steps/compute_cmvn_stats.sh data/test_$testsir exp/make_plp/test_$testsir $plp_dir
    
    
    steps/decode.sh --nj 10 --cmd "$train_cmd" exp/mono_plp_$trainsir/graph data/test_$testsir exp/mono_plp_$trainsir/decode_toydev_$testsir
    
    # Create hypothetic text sequency using decoding output (log files)
    cat exp/mono_plp_$trainsir/decode_toydev_$testsir/log/decode.* | grep "_" | grep -v "LOG" | grep -v "-" | sort > data/test_$testsir/text_plp
    
}
#run_plp

train_pykno() {
    pykno_dir=ssc_pykno
    trainsir=0dB
    . ~/.bashrc
    python local/pykno_feat_extraction.py data/train_$trainsir $pykno_dir
    #~/bin/myJsplit -M 300 -b 1 -n pykno_ssc pykno_jobs.txt
    bash pykno_jobs.txt 
    rm pykno_jobs.txt
    
    cat data/train_$trainsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){$pykno_dir="ssc_pykno/"; print "/home/nxs113020/kaldi-trunk/src/featbin/copy-feats ark,t:${pykno_dir}/$1 ark,scp:${pykno_dir}/$1.ark,${pykno_dir}/$1.scp\n"}' > ark2scp_jobs.txt
    #~/bin/myJsplit -M 300 -b 1 -n pykno_ssc ark2scp_jobs.txt
    bash ark2scp_jobs.txt
    rm ark2sco_jobs.txt
    
    rm data/train_$trainsir/feats.scp
    cat data/train_$trainsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){print `cat ssc_pykno/$1.scp`}' >> data/train_$trainsir/feats.scp
    paste -d ' ' data/train_$trainsir/utt2spk data/train_$trainsir/feats.scp | cut -d ' ' -f 1,4 > tmp
    mv tmp data/train_$trainsir/feats.scp 
    
    #est-pca --dim=20 scp:data/train_$trainsir/feats.scp data/train_$trainsir/pca.mat
    #transform-feats data/train_$trainsir/pca.mat scp:data/train_$trainsir/feats.scp ark,scp:data/train_$trainsir/feats.ark,data/train_$trainsir/feats_pca.scp
    #mv data/train_$trainsir/feats_pca.scp data/train_$trainsir/feats.scp
    
    steps/compute_cmvn_stats.sh data/train_$trainsir exp/make_pykno/train_$trainsir $pykno_dir
    rm -rf exp/mono_pykno_$trainsir
    bash steps/train_mono.sh  --nj 50 --cmd "$train_cmd" data/train_$trainsir data/lang exp/mono_pykno_$trainsir
    utils/mkgraph.sh --mono data/lang exp/mono_pykno_$trainsir exp/mono_pykno_$trainsir/graph 
   
}
#train_pykno

test_pykno(){
    pykno_dir=ssc_pykno
    trainsir=0dB
    . ~/.bashrc
    #Test:    
    python local/pykno_feat_extraction.py data/test_$testsir $pykno_dir
    #~/bin/myJsplit -M 300 -b 1 -n pykno_ssc pykno_jobs.txt
    bash pykno_jobs.txt
    rm pykno_jobs.txt
    
    cat data/test_$testsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){$pykno_dir="ssc_pykno/"; print "/home/nxs113020/kaldi-trunk/src/featbin/copy-feats ark,t:$pykno_dir/$1 ark,scp:$pykno_dir/$1.ark,$pykno_dir/$1.scp\n"}' > ark2scp_jobs.txt
    #~/bin/myJsplit -M 300 -b 1 -n pykno_ssc ark2scp_jobs.txt
    bash ark2scp_jobs.txt
    rm ark2scp_jobs.txt
    
    rm data/test_$testsir/feats.scp
    cat data/test_$testsir/wav.scp | cut -d ' ' -f 1 | perl -ne 'if(m/(\S+)/){print `cat ssc_pykno/$1.scp`}' >> data/test_$testsir/feats.scp
    
    #transform-feats data/train_$trainsir/pca.mat scp:data/test_$testsir/feats.scp ark,scp:data/test_$testsir/feats.ark,data/test_$testsir/feats_pca.scp
    #mv data/test_$testsir/feats_pca.scp data/test_$testsir/feats.scp
    
    steps/compute_cmvn_stats.sh data/test_$testsir exp/make_pykno/test_$testsir $pykno_dir
    steps/decode.sh --nj 10 --cmd "$train_cmd" exp/mono_pykno_$trainsir/graph data/test_$testsir exp/mono_pykno_$trainsir/decode_toydev_$testsir
     
    # Create hypothetic text sequency using decoding output (log files)
    cat exp/mono_pykno_$trainsir/decode_toydev_$testsir/log/decode.* | grep "_" | grep -v "LOG" | grep -v "-" | sort > data/test_$testsir/text_pykno
}
#test_pykno

