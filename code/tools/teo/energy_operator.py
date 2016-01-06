#! /usr/bin/python 
import numpy as np

def teager(x,first_diff=False):
    """ 
    DESA-1 implementation

        If first_diff is On (i.e. True), it means that the function 
        must also calculate the TEO of the first difference signal. 
        """
    y0 = np.multiply(x[1:-1],x[1:-1])-np.multiply(x[2:],x[0:-2])
    
    # Since the since of y0 is two samples fewer than the original signal:
    y0 = np.append(y0,np.array([0,0]))

    if first_diff:
        x_diff = x[1:]-x[:-1]
        y1 = np.multiply(x_diff[1:-1],x_diff[1:-1])-np.multiply(x_diff[2:],x_diff[0:-2])

        # The size of y1 is 3 samples fewer than x, 1 sample for x_diff and 2 samples for calculating the operator.
        y1 = np.append(y1,np.array([0,0,0]))
        return y0,y1
    else:
        return y0,np.array([])


