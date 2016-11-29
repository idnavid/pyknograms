#! /usr/bin/python 

import sys

if __name__=='__main__':
    filename = sys.argv[1]
    fin = open(filename)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0.
    pos = 0.
    neg = 0.
    #data/test_0dB/text_mfcc:t11_swau1a_m34_sgbm3p O C O C
    keys = {'clean':'C','0dB':'O','m3dB':'O','3dB':'O','6dB':'O','m6dB':'O'}
    for i in fin:
        line_list1 = i.strip().split(' ')
        test_key = i.strip().split('_')[1].split('/')[0]
        states = {'O':0,'C':0}
        for j in line_list1[1:]:
            states[j.strip()]+=1
        if states['O']>=states['C']:
            detected='O'
        else:
            detected='C'
        #print i.strip(), 
        #print "detected: %s"%(detected)
        if (keys[test_key]=='O' and detected=='O'):
            tp+=1
            pos+=1
        elif (keys[test_key]=='O' and detected=='C'):
            fn+=1
            pos+=1
        elif (keys[test_key]=='C' and detected=='O'):
            fp+=1
            neg+=1
        elif (keys[test_key]=='C' and detected=='C'):
            tn+=1
            neg+=1
        total+=1.
    
    fin.close()
    print "false alarm:",(100.*fp)/(total)
    print "missed rate:",(100.*fn)/(total)
    print "priors rate:",(100.*pos)/(pos+neg)
    




