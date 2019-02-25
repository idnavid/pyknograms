#! /usr/bin/python 

import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import medfilt
import pylab

from tools.gammatone_fast import applyGammatone


from tools.pykno.instant_amplitude_frequency import am_fm_decomposition


def sfx(pykno_bins_in):
    """
      calculate mean and variance spectral flux (sfx) features for 
      pyknograms. 
        """
    pykno_d0 = pykno_bins_in;
    pykno_d1 = np.roll(pykno_bins_in,1, axis = 0)
    
    mean_sfx = np.mean(np.abs(pykno_d0 - pykno_d1),axis = 1)
    var_sfx = np.var(np.abs(pykno_d0 - pykno_d1), axis = 1)
    return mean_sfx, var_sfx

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


def plot_x_a_f(s,a,f):
    pylab.figure()
    pylab.plot(s)
    pylab.figure()
    pylab.plot(a)
    pylab.figure()
    pylab.plot(f)
    pylab.show()

def pyknogram(file_name,spectogram=False):
    (rate,sig) = wav.read(file_name)
    x = sig.reshape((len(sig),1))
    fs = rate
    window_size = int(0.025*fs)
    shift_size = int(0.010*fs)
     
    nChannels = 120
    cfs = applyGammatone.make_centerFreq(20,3800,nChannels)
    filtered_x,bandwidths = applyGammatone.apply_fbank(x,fs,cfs)
    
    nTime =  1 + np.int(np.floor((len(x) - window_size) / float(shift_size)))
    nFreq = nChannels
    pykno_bins = np.zeros((nTime,nChannels)) # density bins
    tmp = np.zeros((nTime,nChannels))
    for i in range(nChannels):
        a,f = am_fm_decomposition(filtered_x[:,i])
        a[np.where(a>1e5)] = 0
        a_filtered = medfilt(a,11)
        #plot_x_a_f(filtered_x[:,i],a_filtered,f)
        numerator = np.multiply(f,np.power(a,2))
        denominator = np.power(a,2)
        
        framed_num = np.sum(enframe(numerator,window_size,shift_size),axis=1)
        framed_den = np.sum(enframe(denominator,window_size,shift_size),axis=1)
         
        weighted_freqs = fs*np.divide(framed_num,framed_den)
        tmp[:,i] = weighted_freqs
        if not(spectogram):
            candidates = np.where( abs(weighted_freqs-cfs[i]) < bandwidths[i]/5 )
        else:
            candidates = np.where( abs(weighted_freqs-cfs[i]) > 0.1)
        pykno_bins[candidates,i] += np.log(framed_den[candidates]/(np.sqrt(2*bandwidths[i])) + 1e-7)
    return pykno_bins
