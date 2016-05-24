#! /usr/bin/bash

# Convert AMI xml file into text file containing channel (aka speaker) segment start and segment end:
# output:e.g.:
#0 12.05 15.1
cat $1 | grep channel | cut -d '"' -f 4,6,8 | tr '"' ' ' > $2
