#! /usr/bin/python 

import sys
import numpy as np

sys.path.append('/scratch2/nxs113020/pyknograms/code/tools/pykno/')
from pyknogram_extraction import *


def extract_pykno(wav_id, wav_file,feat_dir):
    fout = open(feat_dir+'/'+wav_id,'w')
    for i in range(1):
        pykno = pyknogram(wav_file)
        fout.write(wav_id+' [ ')
        for j in pykno:
            for k in j.tolist():
                fout.write(str(k)+' ')
            fout.write('\n')
        fout.write(' ]\n')
    fout.close()


if __name__=='__main__':
    data_dir = sys.argv[1].strip()+'/'
    feature_dir = sys.argv[2].strip()+'/'
    scp_file = data_dir+'wav.scp'
    fin = open(scp_file)
    fjobs = open('pykno_jobs.txt','w')
    for i in fin:
        line_list = i.strip().split(' ')
        cmd = "python -c \"import sys;sys.path.append(\'%s\');from pykno_feat_extraction import *;extract_pykno(\'%s\',\'%s\',\'%s\')\"\n"
        fjobs.write(cmd%('/scratch2/nxs113020/pyknograms/code/kaldi_setup/local/',line_list[0],line_list[1],feature_dir))
    fjobs.close()
    fin.close()





