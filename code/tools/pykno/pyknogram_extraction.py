#! /usr/bin/python 

import numpy as np
import sys
import scipy.io.wavfile as wav
from scipy.signal import medfilt
import pylab

sys.path.append('/scratch2/nxs113020/pyknograms/code/tools/gammatone_fast')
from applyGammatone import *


from instant_amplitude_frequency import am_fm_decomposition

def enframe(x, winlen, hoplen):
    """
      receives a 1D numpy array and divides it into frames.
      outputs a numpy matrix with the frames on the rows.
        """
    x = np.squeeze(x)
    if x.ndim != 1: 
        raise TypeError("enframe input must be a 1-dimensional array.")
    n_frames = 1 + np.int(np.floor((len(x) - winlen) / float(hoplen)))
    xf = np.zeros((n_frames, winlen))
    for ii in range(n_frames):
        xf[ii] = x[ii * hoplen : ii * hoplen + winlen]
    return xf





if __name__=='__main__':
    (rate,sig) = wav.read("/corpora/timit/all_8k/fadg0/sa1-fadg0.wav")
    x = sig.reshape((len(sig),1))
    fs = rate
    window_size = int(0.025*fs)
    shift_size = int(0.010*fs)
    
    nChannels = 40
    cfs = make_centerFreq(20,3800,nChannels)
    filtered_x = apply_fbank(x,fs,cfs)
    
    nTime =  1 + np.int(np.floor((len(x) - window_size) / float(shift_size)))
    nFreq = nChannels
    f_bins = np.zeros((nTime,nFreq))
    for i in range(40):
        a,f = am_fm_decomposition(filtered_x[:,i])
        a[np.where(a>1e5)] = 0
        a_filtered = medfilt(a,11)
        
        numerator = np.multiply(f,np.power(a,2))
        denominator = np.power(a,2)
        
        framed_num = np.sum(enframe(numerator,window_size,shift_size),axis=1)
        framed_den = np.sum(enframe(denominator,window_size,shift_size),axis=1)
        
        weighted_freqs = fs*np.divide(framed_num,framed_den)

        k = 0
        for j in weighted_freqs:
            if abs(j-cfs[i])<0.05*cfs[i]:
                f_bins[k,i] = 1
            k+=1
    pylab.imshow(f_bins.T,aspect='auto')
    pylab.show()

   
