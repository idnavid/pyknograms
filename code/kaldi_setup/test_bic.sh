
. path.sh
. cmd.sh
train_cmd=run.pl
run_mfcc(){
    mfccdir=mfcc
    for x in toy_3; do
      steps/make_mfcc.sh --cmd "$train_cmd" --nj 1 data/$x exp/make_mfcc/$x $mfccdir || exit 1;
      steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x $mfccdir || exit 1;
    done
}
#run_mfcc


make_ref(){
    ami_annotated_segment=/home/nxs113020/Downloads/ami_dir/segments

    for x in toy_3; do
        local/make_ami_ref.sh data/$x $ami_annotated_segment exp/ref/$x
    done

}
#make_ref

run_changedetection() {

    for x in toy_3; do
       local/change_detect_bic.sh data/$x exp/ref/$x exp/change_detect/$x
    done

}
run_changedetection

