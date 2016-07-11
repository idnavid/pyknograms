
import pylab
import sys
import numpy as np

sys.path.append('../tools/pykno')
from pyknogram_extraction import *


wav_id = sys.argv[1]
wav_name = sys.argv[2]

pykno = pyknogram(wav_name)
pylab.imshow((pykno.T + 1e-7),aspect='auto')
pylab.show()

m1, v1 = sfx(pykno)

#pylab.plot(np.log(m1+1e-7))
#pylab.figure()
#pylab.plot(np.log(v1+1e-7))
#pylab.figure()
