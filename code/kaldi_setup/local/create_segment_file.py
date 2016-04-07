#! /usr/bin/python

import sys
import subprocess

def length_to_segment(fileid, filename):
    dir = '/erasable/nxs113020/ssc_files/'
    fseg = open(dir+fileid.strip()+'.seg','w')
    ftext =open(dir+fileid.strip()+'.txt','w')
    fs = 8000.
    start_time = 0.000
    output = subprocess.check_output("soxi "+filename,shell=True)
    output_list = output.split('\n')
    for i in output_list:
        if 'Duration' in i:
            nsamples = int(i.split('=')[-1].split('samples')[0].strip())
            end_time = nsamples/fs
    start_string = "%07d"%(1000*start_time)
    end_string = "%07d"%(1000*end_time)
    fseg.write(fileid+'_'+start_string+'_'+end_string+' '+fileid+' '+str(start_time)+' '+str(end_time)+'\n')
    if fileid[0]=='t':
        ftext.write(fileid+'_'+start_string+'_'+end_string+' '+'O'+'\n') # O: overlap
    elif fileid[0]=='s':
        ftext.write(fileid+'_'+start_string+'_'+end_string+' '+'C'+'\n') # C: clean
    fseg.close()
    ftext.close()

if __name__=='__main__':
    main_dir = "/scratch2/nxs113020/pyknograms/code/kaldi_setup/"
    fin = open(main_dir+'data/train_0dB/wav.scp')
    fjobs = open('segment_jobs.txt','w')
    for l in fin:
        line_list = l.split(' ')
        wavid = line_list[0].strip()
        wavpath = line_list[1].strip()
        fjobs.write("python -c \"import sys;sys.path.append(\'%s/local/\');from create_segment_file import *;length_to_segment(\'%s\',\'%s\') \"\n"%(main_dir,wavid,wavpath))
    fjobs.close()
    
