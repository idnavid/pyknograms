#! /usr/bin/bash

cat data/train/wav.scp | perl -ne 'if(m/(\S+)\s(\S+)/){print ". ~/.bashrc; python /scratch2/nxs113020/pyknograms/code/kaldi_setup/local/pykno_feat_extraction.py $_"}' > train_pykno_jobs.txt
