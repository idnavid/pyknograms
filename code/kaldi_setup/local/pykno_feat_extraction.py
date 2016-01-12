#! /usr/bin/python 

import sys
import numpy as np

sys.path.append('/scratch2/nxs113020/pyknograms/code/tools/pykno/')
from pyknogram_extraction import *



wav_id = sys.argv[1] 
wav_file = sys.argv[2]
fout = open('/erasable/nxs113020/pyknograms/'+wav_id,'w')
for i in range(1):
    pykno = pyknogram(wav_file)
    fout.write(wav_id+' [ ')
    for j in pykno:
        for k in j.tolist():
            fout.write(str(k)+' ')
        fout.write('\n')
    fout.write(' ]\n')
fout.close()

