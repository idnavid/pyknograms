#! /usr/bin/python 

import numpy as np
import sys
import scipy.io.wavfile as wav
from scipy.signal import medfilt
import pylab

sys.path.append('/scratch2/nxs113020/pyknograms/code/tools/gammatone_fast')
from applyGammatone import *


from instant_amplitude_frequency import am_fm_decomposition



if __name__=='__main__':
    (rate,sig) = wav.read("/scratch2/nxs113020/pyknograms/selection.wav")
    x = sig.reshape((len(sig),1))
    fs = rate
    cfs = make_centerFreq(20,3800,40)
    filtered_x = apply_fbank(x,fs,cfs)
    for i in range(40):
        a,f = am_fm_decomposition(filtered_x[:,i])
        a[np.where(a>1e5)] = 0
        a_filtered = medfilt(a,11)
        pylab.plot(filtered_x[:,i])
        pylab.plot(a_filtered)
        pylab.show()
