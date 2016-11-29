
import pylab
import sys
import numpy as np

sys.path.append('tools/pykno')
from pyknogram_extraction import *


wav_id = sys.argv[1]
wav_name = sys.argv[2]
pykno1 = pyknogram(wav_name,spectogram=True)
pykno = pyknogram(wav_name)
m1, v1 = sfx(pykno)
pylab.imshow(np.flipud(pykno1.T + 1e-7),aspect='auto')
pylab.imshow(np.flipud(pykno.T + 1e-7),aspect='auto',cmap='Blues',alpha=0.7)
#pylab.plot(m1,color='g',linewidth=2)
#pylab.plot(v1,color='r',linewidth=2)
pylab.show()



#pylab.figure()
#pylab.plot(np.log(v1+1e-7))
#pylab.figure()
