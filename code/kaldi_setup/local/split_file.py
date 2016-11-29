#! /bin/bash

# Split an input feature file and its corresponding 
# labels into smaller chunks. 

import sys
import os

def vector_to_matrix(label_file,out_labels):
    cmd = "cat %s "
    cmd += "| sed 's/\[ /\[/g' "
    cmd += "| sed 's/ \]/\]/g' "
    cmd += "| tr ' ' '\\n' "
    cmd += "| sed 's/\\n\\n\\n\[/ \[/g' "
    cmd += "| sed 's/\]/ \]/g' "
    cmd += "| sed 's/\\n\\n/ /g' "
    cmd += "| sed '/^$/d' " # remove empty lines
    cmd += "| sed 's/\[/\[ /g' "
    cmd += " >> %s"
    os.system(cmd%(label_file,out_labels))

data_dir=sys.argv[1]
out_dir=data_dir+'/chunks'
tmp = data_dir.split('/')
if (tmp[-1]==''):
    ref_dir='exp/ref/'+tmp[-2]
else:
    ref_dir='exp/ref/'+tmp[-1]

os.system('mkdir -p '+out_dir)


fin = open(data_dir+'/wav.scp')
out_segments = out_dir+'/segments'
out_labels = out_dir+'/labels.ark'
os.system('rm '+out_labels)
fout = open(out_segments,'w')
for x in fin:
    utt_id = x.split(' ')[0]
    session=utt_id.split('.')[0]
    label_file=ref_dir+'/labels/'+session+'.label'
    vector_to_matrix(label_file,out_labels)
    # convert vector to matrix:
    flabels = open(label_file)
    for i in flabels:
        labels = i.split('[')[-1].strip().split(']')[0].strip().split(' ')
        end_time = len(labels)*0.01
    start_time = 0.0
    seg_size = 60.0*5 # 5 minute segments
    while (start_time < end_time):
        seg_id = utt_id+'_%07d'%(int(1000*start_time))+'_%07d'%(int(1000*end_time))
        fout.write('%s %s %.3f %.3f'%(seg_id, utt_id, start_time, end_time)+'\n')
        start_time+=seg_size
    flabels.close()
fin.close()
fout.close()

feats_scp = data_dir+'/feats.scp'
out_ark = out_dir+'/feats.ark'
out_scp = out_dir+'/feats.scp'
os.system('. path.sh; extract-feature-segments scp:%s %s ark,scp:%s,%s'%(feats_scp,out_segments,out_ark,out_scp))
splitted_labels_ark=out_dir+'/splitted_labels.ark'
os.system('. path.sh; extract-feature-segments ark:%s %s ark,t:%s'%(out_labels,out_segments,splitted_labels_ark))

