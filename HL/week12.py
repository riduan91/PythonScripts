# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 14:11:07 2017

@author: ndoannguyen
"""

import pandas as pd

data = pd.read_excel("test.xlsx") #chergement du fichier Excel

mymax = max(data["Contrainte conv. (MPa) moyenne mobile"])
data = data[data["Allong. plast. conv. (-)"] > 0.0002]
data = data[data["Contrainte conv. (MPa) moyenne mobile"] < mymax]
