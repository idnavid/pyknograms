HMM-based overlap detection system. 
Three features were used here: MFCC, PLP, Pyknograms.

System outputs are stored in data/test_[SIR:clean/0dB/...]/text_[mfcc/plp/pykno]
To score systems, use the script in run.sh 
bash run.sh [SIR:clean/0dB]
Once calculated for all desired SIR values, summarize all outputs in a single file. 
grep "." data/test_*/text_mfcc > mfcc_scores

To get FA and MR, use local/find_accuracy.py 

python local/find_accuracy.py mfcc_scores



