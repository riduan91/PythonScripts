# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:21:44 2017

@author: ndoannguyen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.ticker import LinearLocator, FormatStrFormatter
#from matplotlib import collections  as mc

#def f(a,b):
#    return 0.41*a - 0.92*b + 12.5


dataset = pd.read_csv('LinearRegressionData_Gaussian.txt', sep = '\t', names = ["coordinate1", "coordinate2", "value"])
#dataset = pd.read_csv('LinearRegression/LinearRegressionData_Uniform.txt', sep = '\t', names = ["coordinate1", "coordinate2", "value"])

data_features = dataset.iloc[:, :-1].values
data_values = dataset.iloc[:, 2].values

def LinearRegressionTrain(X, y):
    return np.linalg.inv((X.transpose()*X))*X.transpose()*y

def LinearRegressionPredict(w, x):
    return np.matrix(x)*w

# We want to find a, b, c such that y = ax1 + bx2 + c. Write W = (a, b, c) transpose, x = (x1, x2, 1)

X = np.matrix(np.insert(data_features, 2, 1, axis=1))
y = np.matrix(data_values).transpose()

w = LinearRegressionTrain(X, y)
print "Coefficients and intercept: ", w.transpose()[0,:]

PredictZ = np.array(LinearRegressionPredict(w, X))

# Plotting part



planX = np.arange(0, 5, 0.25)
planY = np.arange(0, 5, 0.25)
planX, planY = np.meshgrid(planX, planY)
planZ = w[0,0] * planX + w[1,0] * planY + w[2,0]

limit=min(50, len(data_values))
# Comment this line to hide real data
fig = plt.figure(figsize=(15,10))
ax = fig.gca(projection='3d')
ax.scatter(data_features[:limit,0], data_features[:limit,1], data_values[:limit], color="blue", label='Real Values')

ax.scatter(data_features[:limit,0], data_features[:limit,1], PredictZ[:limit,0], color="green", label='Prediction')
ax.plot_surface(planX, planY, planZ, color="yellow", alpha=.2)
ax.set_zlim(min(data_values), max(data_values))
ax.legend()
for i in range(limit):
    ax.plot([data_features[i,0], data_features[i,0]], [data_features[i,1], data_features[i,1]], [data_values[i], PredictZ[i,0]], color = "black", linestyle = '-.')
plt.show()


#-------------------

from sklearn import linear_model

LinearRegressionModel = linear_model.LinearRegression(fit_intercept = True)
LinearRegressionModel.fit(data_features, data_values)
print "Coefficients: ", LinearRegressionModel.coef_
print "Intercept: ", LinearRegressionModel.intercept_
