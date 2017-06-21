# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:22:35 2017

@author: HL247224
"""
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D


def func(X, a, b, c, d, e, f):
    x,y = X
    return a + b*x + c*y + d*x*y + e*x**2 + f*y**2

data = pd.read_excel('G74_Rm_2.xlsx') #chergement du fichier Excel

R_m = data['Rm'].values #selection de la variable, chargement dans une numpy array
x = data['Temperature'].values
y = data['Hydrogen'].values

#plt.plot(R_m, x, y, 'b-', label = 'data')

#Fit for the parameters a, b, c of the function func
popt, pcov = curve_fit(func, (x,y), R_m)

print "Paramètres: ", popt
#plt.plot((x, y), func((x, y), *popt), 'r-', label = 'fit')

#plt.show()

##################################
############PLOTTING##############

zone_x = np.arange(-100, 800, 20)
zone_y = np.arange(-500, 3500, 50)
zone_x, zone_y = np.meshgrid(zone_x, zone_y)
zone_z = func((zone_x, zone_y), *popt)

fig = plt.figure(figsize=(15,10))
ax = fig.gca(projection='3d')
size = len(R_m)

ax.scatter(x, y, R_m[:size], color="blue", label='Real Values')
ax.scatter(x, y, func((x, y), *popt), color="green", label='Prediction')

ax.plot_surface(zone_x, zone_y, zone_z, color="yellow", alpha=.2)
ax.legend()
for i in range(size):
    ax.plot([x[i], x[i]], [y[i], y[i]], [R_m[i], func((x, y), *popt)[i]], color = "black", linestyle = '-.')
plt.show()

