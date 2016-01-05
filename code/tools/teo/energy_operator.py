#! /usr/bin/python 
import numpy as np

def teager(x):
    """ 
    DESA-1 implementation
        """
    y = np.multiply(x[1:-1],x[1:-1])-np.multiply(x[2:],x[0:-2])
    return y


