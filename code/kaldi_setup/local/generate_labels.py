#! /usr/bin/python

import sys
import commands
import os

wavscp = sys.argv[1]
annotations_dir = sys.argv[2]
file_dump = sys.argv[3]
fjobs = open(file_dump+"/xml2txt.jobs",'w')
flabels = open(file_dump+"/seg2labels.jobs",'w')


fin = open(wavscp)
for i in fin:
    line = i.strip()
    line_list = line.split(' ')
    base_name = line_list[0]
    session = base_name.split('.')[0]
    for j in line_list:
        if ".wav" in j:
            wavfile = j.strip()
    # 1. Generate txt files from segment xml:
    shell_cmd = "ls "+annotations_dir+"/"+session+"*"
    p = commands.getstatusoutput(shell_cmd)
    files = p[1].split('\n')
    fout = open(file_dump+"/segmentTXT_"+session+".txt",'w')
    for j in files:
        base_name = j.split('/')[-1].split('.xml')[0]
        txt_name = file_dump+base_name+'.txt'
        shell_cmd = "bash local/segXML2TXT.sh "+j+" "+txt_name
        fjobs.write(shell_cmd+'\n')
        fout.write(txt_name+"\n")
    fout.write(wavfile+"\n")
    fout.close()
    
    shell_cmd = "python local/seg2frame.py "+ file_dump+"/segmentTXT_"+session+\
                ".txt "+file_dump+"/"+session+".label 0"
    flabels.write(shell_cmd+"\n")
flabels.close()
fjobs.close()

