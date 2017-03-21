This project is a python implementation of pyknogram extraction. 
Pyknograms are a modified verision of the STFT that emphasize more on
the harmonic structure of speech. 
This work is used for co-channel speech analysis. 
A detailed description of the algorithm is presented in "Teager-Kaiser Energy Operators for Overlapped Speech Detection," Shokouhi, Hansen. IEEE/ACM Trans. on ASLP. 

Prereqs:
    numpy
    scipy
    pylab

The directory "code" contains an example script (example.py) that calculates pyknograms 
for the wavefile selection.wav

Run the following inside the code directory:
$python example.py selection ../selection.wav

Outputs will be:
    figure1 : pyknogram
    figure2 : mean(spectral flux of pyknograms)
    figure3 : var(spectral flux)

Navid Shokouhi
December 2015
