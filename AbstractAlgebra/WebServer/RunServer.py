# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 18:21:07 2017

@author: ndoannguyen
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import Flask, render_template, request
app = Flask(__name__)

BASIC_SOURCE_DIR = "../"
import sys

sys.path.append(BASIC_SOURCE_DIR)
from ParseExpression import MyBigradedAlgebra, MyFreeBigradedModuleOverAlgebra
from Test import process
import multiprocessing

TIMEOUT = 240
OPERATIONS = {
                'simplification': 'Simplification',
                'addition': 'Addition',
                'substraction': 'Substraction',
                'multiplication': 'Multiplication',
                'bidegree_calculation': 'Bidegree Calculation'
             }
             
NB_INPUT_OF_OPERATIONS = {
                'simplification': ['simplification_element_1'],
                'addition': ['addition_element_1', 'addition_element_2'],
                'substraction': ['substraction_element_1', 'substraction_element_2'],
                'multiplication': ['multiplication_element_1', 'multiplication_element_2'],
                'bidegree_calculation': ['bidegree_calculation_element_1']
             }

@app.route("/")
def app1():
   return render_template("app1.html")

@app.route("/describe_module", methods = ['POST', 'GET'])
def describe_module():
    if request.method == 'POST':
        parameters = request.form
        result_queue = multiprocessing.Queue()
        p = multiprocessing.Process(target = describe_module_core, args = (parameters, result_queue))
        p.start()
        try:
            s = result_queue.get(True, TIMEOUT)
        except:
            s = "Timeout. Please choose smaller m, n."
            p.terminate()
            p.join()
        #p.join(TIMEOUT)
        
        return render_template("result1.html", result = (parameters, s.split("\n")))

    else:
        return render_template("app1.html")

def describe_module_core(parameters, result_queue):
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
    result_queue.put(s)

@app.route("/app2")
def app2():
   return render_template("app2.html")

@app.route("/do_operation", methods = ['POST', 'GET'])
def do_operation():
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
        
        if (parameters['chosen_operation'] == 'Simplification'):
            results = alg.simplify(parameters['simplification_element_1'])
        
        elif (parameters['chosen_operation'] == 'Addition'):
            results = alg.add(parameters['addition_element_1'], parameters['addition_element_2'])
        
        elif (parameters['chosen_operation'] == 'Substraction'):
            results = alg.substract(parameters['substraction_element_1'], parameters['substraction_element_2 '])
        
        elif (parameters['chosen_operation'] == 'Multiplication'):
            results = alg.multiply(parameters['multiplication_element_1'], parameters['multiplication_element_2'])
                
        elif (parameters['chosen_operation'] == 'Bidegree Calculation'):
            results = alg.getBidegree(parameters['bidegree_calculation_element_1'])
        
        else:
            results = []
        return render_template("result2.html", result = (parameters, OPERATIONS, NB_INPUT_OF_OPERATIONS, results))
    else:
        return render_template("app2.html")



port = 8801
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8801, debug=True)
