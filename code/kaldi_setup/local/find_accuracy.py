#! /usr/bin/python 

import sys

if __name__=='__main__':
    filename = sys.argv[1]
    label = sys.argv[2]
    fin = open(filename)
    correct = 0
    error = 0
    for i in fin:
        line_list = i.strip().split(' ')
        states = {'O':0,'C':0}
        for j in line_list[1:]:
            states[j.strip()]+=1
        if states['O']>=states['C']:
            detected='O'
        else:
            detected='C'
        if label==detected:
            correct +=1
        else:
            error +=1
    fin.close()
    print "percent correct:",(100.*correct)/(error+correct)




