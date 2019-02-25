import pylab
import sys
import numpy as np

from tools.pykno import pyknogram_extraction

wav_id = sys.argv[1]
wav_name = sys.argv[2]
pykno = pyknogram_extraction.pyknogram(wav_name)
m,v = pyknogram_extraction.sfx(pykno)
print(wav_id,np.mean(m), np.mean(v))

