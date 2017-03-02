# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:11:41 2017

@author: ndoannguyen
"""

import numpy as np
mysize = 10000

def generateData():
    noise = np.random.normal(loc=0.0, scale=1.0, size=mysize)
    X1 = np.random.uniform(low=0.0, high=4.0, size=mysize)
    X2 = np.random.uniform(low=0.0, high=4.0, size=mysize)
    a = 0.41
    b = 0.92
    c = 12.5
    return X1, X2, a*X1 + b*X2 + c + noise

f = open("LinearRegressionData_Gaussian.txt", 'w')
data = generateData()
for i in range(mysize):
    f.write(str(round(data[0][i],2)) + "\t" + str(round(data[1][i],2)) + "\t" + str(round(data[2][i], 4)) + "\n")
f.close()