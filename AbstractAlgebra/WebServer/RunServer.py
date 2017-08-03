# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 18:21:07 2017

@author: ndoannguyen
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import Flask, render_template, request
app = Flask(__name__)

BASIC_SOURCE_DIR = "D:/Userfiles/ndoannguyen/Documents/Python Scripts/AbstractAlgebra"
import sys

sys.path.append(BASIC_SOURCE_DIR)
from ParseExpression import MyBigradedAlgebra, MyFreeBigradedModuleOverAlgebra
from Test import process

@app.route("/")
def app1():
   return render_template("app1.html")

@app.route("/describe_module", methods = ['POST', 'GET'])
def describe_module():
    if request.method == 'POST':

        parameters = request.form
        alg_generators = parameters['alg_generators'].replace(" ", "").split(",")
        alg_bidegree_strings = parameters['alg_bidegrees'].replace(" ", "").split("),(")
        alg_bidegrees = []
        for string in alg_bidegree_strings:
            bidegree = map(int, string.replace("(", "").replace(")", "").split(","))
            alg_bidegrees.append(bidegree)
        alg_relations = parameters['alg_relations'].replace(" ", "").split(",")
        
        alg = MyBigradedAlgebra(alg_generators, alg_bidegrees, alg_relations, True)

        
        mod_generators = parameters['mod_generators'].replace(" ", "").split(",")
        mod_bidegree_strings = parameters['mod_bidegrees'].replace(" ", "").split("),(")
        mod_bidegrees = []
        for string in mod_bidegree_strings:
            bidegree = map(int, string.replace("(", "").replace(")", "").split(","))
            mod_bidegrees.append(bidegree)
        mod = MyFreeBigradedModuleOverAlgebra(mod_generators, mod_bidegrees, alg)

        actions = parameters['actions'].replace(" ", "").split(",")
        
        limit_x = parameters['limit_x']
        limit_y = parameters['limit_y']
        
        s = process(mod, actions, "output.txt", int(limit_x), int(limit_y))
        
        return render_template("result1.html", result = (parameters, s.split("\n")))

    else:
        return render_template("app1.html")
    
port = 8801
if __name__ == '__main__':
    app.run(port = 8801, debug=True)