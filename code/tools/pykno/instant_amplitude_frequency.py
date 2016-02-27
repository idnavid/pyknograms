#! /usr/bin/python 

import numpy as np
import sys

sys.path.append('tools/teo')
from energy_operator import teager
def am_fm_decomposition(x):
    """
        returns 
        f: instantaneous frequency per sample
        a: instantaneous amplitude per sample
        """
    y0,y1 = teager(x,first_diff=True)
    # y0: TEO of x(n)
    # y1: TEO of the x(n) - x(n-1)
    
    arccos_arg = 1 - np.divide(y1,2*y0 + 1e-7)
    arccos_arg[np.where(arccos_arg > 1)] = 1
    arccos_arg[np.where(arccos_arg < -1)] = -1
    f = (0.5/np.pi)*np.arccos(arccos_arg)
    a = np.sqrt(abs(np.divide(y0,1e-7+np.power(np.sin(2*np.pi*f),2))))
    return a, f
