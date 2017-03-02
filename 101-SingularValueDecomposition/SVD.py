# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 11:29:17 2017

@author: ndoannguyen
"""

import numpy as np

A = np.matrix([[1, -1, 2], [-3, 5, 2]])
U, S, V = np.linalg.svd(A)

# Check that A = U * S * V
print U * np.matrix([[S[0],0,0],[0,S[1],0]]) * V

#7X5029
#keon
#amadeus01