#! /usr/bin/python
import sys
import numpy as np
import commands 
import pylab 
import os

# python seg2frame.py scpfile outfile 0/1 
# scpfile include (segmentfilenames + wavfilename)
# 0 for not plot; 1 for plot
# outfile: destination to write as kaldi ark format

def time2frame(s,e,inc):
    s_f = int(s/inc)
    e_f = int(e/inc)+1
    return s_f, e_f

if __name__=='__main__':
    fs = 16000.
    inc = 0.01
    win = 0.025
    filename = sys.argv[1]
    filenameOutput = sys.argv[2]
    PLOT = int(sys.argv[3])
    fin = open(filename)
    fout = open(filenameOutput,'w')
    session_txt = []
    session_wav = []
    for i in fin:
        if not(".wav" in i):
            session_txt.append(i.strip())
        else:
            session_wav.append(i.strip())
    soxi_out = commands.getstatusoutput("soxi "+session_wav[0].strip())[1].split('\n')
    for i in soxi_out: 
        if "Duration" in i:
            wav_length = int(i.split('samples')[0].strip().split(' ')[-1])
    
    # find total number of samples
    n_frames = 1 + (wav_length-int(fs*win))/int(inc*fs)
    
    
    all_files = {}
    for i in range(len(session_txt)):
        all_files[i] = np.zeros((n_frames,1))

    for i in session_txt:
        line = i.strip()
        for j in open(line):
            line_list = j.strip().split(' ')
            for k in line_list:
                try:
                    channel = int(line_list[0])
                    start_t = float(line_list[1])
                    end_t   = float(line_list[2])
                except:
                    channel = int(line_list[2])
                    start_t = float(line_list[0])
                    end_t   = float(line_list[1])
            start_f,end_f = time2frame(start_t,end_t,inc)
            all_files[channel][start_f:end_f] = 1

    labels = all_files[0]
    # find overlaps
    for i in all_files:
        if i!=0:
            labels += all_files[i]
    n = len(all_files)*(len(all_files)+1)/2
    # replace overlaps with large number n
    labels[np.where(labels>1)] = -1*n
    labels[np.where(labels!=-1*n)] = 0
    # select different value for each channel
    for i in all_files:
        labels += (i+1)*all_files[i]

    
    labels[np.where(labels<0)] = -1
    del all_files
    if PLOT == 1:
        pylab.plot(labels)
        pylab.show()
    
    uttid = os.path.splitext(os.path.basename(session_wav[0]))[0]
    fout.write(uttid);
    fout.write("  [ ")
    labels.tofile(fout, " ", format="%i")
    fout.write(" ]")
    fout.write("\n")
    fout.close()
