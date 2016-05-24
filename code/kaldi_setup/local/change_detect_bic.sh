#! /bin/bash

data_dir=$1
ref_dir=$2 # ground-truth
out_dir=$3 # bic decisions

bin_dir=/home/nxs113020/CRSSdiar/src/diarbin/

if [ -d $out_dir ]; then
    rm -rf $out_dir
fi
mkdir -p $out_dir/tmp
mkdir -p $out_dir/segments

#while read x;do
#    #cat $x >> $out_dir/tmp/labels.ark
#done<$ref_dir/labels/labels.scp

#copy-vector scp:exp/vad/toy/vad_toy.1.scp ark,t:$out_dir/tmp/labels.ark
#copy-vector scp:labels.scp ark,t:$out_dir/tmp/labels.ark
#copy-vector ark:lab ark,t:$out_dir/tmp/labels.ark

$bin_dir/changeDetectBIC scp:$data_dir/feats.scp scp:$ref_dir/vad_label/vad_labels.scp $out_dir/segments
rm -rf $out_dir/tmp
