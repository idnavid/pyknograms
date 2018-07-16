## Unsupervised overlap detection for single channel speech
This project is a python implementation of pyknogram extraction. 
Pyknograms are a modified verision of the STFT that emphasize more on
the harmonic structure of speech. 
This work is used for co-channel speech analysis. 
Feel free to reach out if you need help to run this code. 

### Citations:
A detailed description of the algorithm is presented in our Transactions paper. Please cite:

[1] "Teager-Kaiser Energy Operators for Overlapped Speech Detection," Shokouhi, Hansen. IEEE/ACM Trans. on ASLP, 2017. <br/>
[2] "Robust Overlapped Speech Detection and its Application in Word-Count Estimation for Prof-Life-Log Data," Shokouhi, Ziaei, Sangwan, Hansen, ICASSP, 2015. <br/>

- Prereqs:
    - numpy
    - scipy
    - pylab

The directory "code" contains an example script (example.py) that calculates pyknograms 
for the wavefile selection.wav

Run the following inside the code directory:

$python example.py selection ../selection.wav

Outputs will be:
    - figure1 : pyknogram
    - figure2 : mean(spectral flux of pyknograms)
    - figure3 : var(spectral flux)

Navid Shokouhi

December 2015
