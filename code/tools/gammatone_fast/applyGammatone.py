#! /usr/bin/python 

# Python implementation of gammatone based on the MATLAB code by:  Christopher Hummersone
# Link to original source: http://www.mathworks.com/matlabcentral/fileexchange/32212-gammatone-filterbank
#
# Navid Shokouhi - January 2016 

import numpy as np
import scipy.signal
import scipy.io.wavfile as wav
import pylab 

def apply_fbank(x,fs,cfs,align=False,hilbert_envelope=False):
    """
        x:        input signal (numpy array)
        fs:       sampling rate (integer)
        cfs:      center frequencies (numpy array)
        align:    allow phase alignment across filters. 
        """
    n_channels = len(cfs)
    filterOrder = 4
    gL = int(0.128*fs) # minimum filter length is 128 msec. This must be a power of 2. 
    b = 1.019*24.7*(4.37*(cfs/1000)+1); # rate of decay or bandwidth
    gt = np.zeros((gL,n_channels));  # Initialise IR
    tc = np.zeros(cfs.shape);  # Initialise time lead
    phase = 0

    tpt = (2*np.pi)/fs
    gain = ((1.019*b*tpt)**filterOrder)/6; # based on integral of impulse

    tmp_t = np.array([range(gL)])*1.0/fs

    # calculate impulse responses:
    y = np.zeros((len(x)+gL-1,n_channels))
    for i in range(n_channels):
        gain_term = gain[i]*fs**3
        poly_term = tmp_t**(filterOrder-1)
        damp_term = np.exp(-2*np.pi*b[i]*tmp_t)
        oscil_term = np.cos(2*np.pi*cfs[i]*tmp_t+phase)
        gt[:,i] = gain_term*poly_term*damp_term*oscil_term; 
        bm = scipy.signal.fftconvolve(x,gt[:,i].reshape((gL,1)))
        y[:,i] = bm[:,0]

        if hilbert_envelope:
            bm_hilbert = scipy.signal.hilbert(bm[:,0])
            y[:,i] = abs(bm_hilbert)

    return y

def ErbRateToHz(erb):
    return (10**(erb/21.4)-1)/4.37e-3

def HzToErbRate(hz):
    return (21.4*np.log10(4.37e-3*hz+1))

def make_centerFreq(minCf,maxCf,n_channels):
    return ErbRateToHz(np.linspace(HzToErbRate(minCf),HzToErbRate(maxCf),n_channels));

if __name__=='__main__':
    (rate,sig) = wav.read("/corpora/timit/all_8k/fadg0/sa1-fadg0.wav")
    x = sig.reshape((len(sig),1))
    fs = rate
    cfs = make_centerFreq(20,3800,100)
    filtered_x = apply_fbank(x,fs,cfs)
    #pylab.imshow(filtered_x[:,::-1].T,aspect='auto')
    for i in range(40):
        pylab.plot(filtered_x[:,i]/abs(max(filtered_x[:,i])) + i)
    pylab.show()
