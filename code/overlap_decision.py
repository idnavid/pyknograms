import pylab
import sys
import numpy as np

sys.path.append('/scratch2/nxs113020/pyknograms/code/tools/pykno')
from pyknogram_extraction import *

wav_id = sys.argv[1]
wav_name = sys.argv[2]
pykno = pyknogram(wav_name)
m,v = sfx(pykno)
print wav_id,np.mean(m), np.mean(v)

