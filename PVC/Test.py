# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:17:26 2017

@author: ndoannguyen
"""
import time

from ParseExpression import MyBigradedAlgebra, MyFreeBigradedModuleOverAlgebra
from PlotBidegreeTable import writeToTex, plotAction

def process(mymod, actions, outputfile, limit_x=5, limit_y=5):
    myalg = mymod.myalg
    print "Algebra of generators %s of degree %s and relations %s" % (", ".join(myalg.variables),  ", ".join(map(str, myalg.alg.bidegrees)), ", ".join(myalg.relation_strings))
    if len(myalg.variables) <= 1 or myalg.alg.commutative:
        print "It is commutative"
    elif len(myalg.variables) >= 2 and not myalg.alg.commutative:
        print "It may not be commutative"
    print "Module of generators %s of degree %s." % (", ".join(mymod.variables), ", ".join(map(str, mymod.mod.bidegrees)))
    print "Actions: %s" % (", ".join(actions))
    
    alg = mymod.mod.algebra

    limit = [0] * alg.nb_generators
    for i in range(len(limit)):
        if alg.bidegrees[i][0] != 0 and alg.bidegrees[i][1] != 0:
            limit[i] = 2 * max(abs(limit_x / alg.bidegrees[i][0]) , abs(limit_y / alg.bidegrees[i][1]) ) 
        elif alg.bidegrees[i][0] != 0:
            limit[i] = 2 * abs(limit_x / alg.bidegrees[i][0]) 
        elif alg.bidegrees[i][1] != 0:
            limit[i] = 2 * abs(limit_y / alg.bidegrees[i][1]) 
    
    print "limit", limit
        
    source_bidegrees = mymod.mod.possibleBidegreesOfLimit(limit)
    writeToTex(mymod, source_bidegrees, actions, limit_x, limit_y, outputfile)
    plotAction(mymod, source_bidegrees, actions, limit_x, limit_y)
    
    print "-------------------------------------------------"


#TEST1
"""
t0 = time.time()
myalg = MyBigradedAlgebra(["x", "y", "z", "t"], [(20, 4), (24, 0), (3, 1), (-24, 0)], ["z^3=0"], True)
mymod = MyFreeBigradedModuleOverAlgebra(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], [(0, 0), (5, 1), (6, 0), (11, 1), (12, 0), (17, 1), (18, 0), (23, 1)], myalg)
actions = [ "z", "x*z*t" ]
process(mymod, actions, 'output.tex', 48, 24)
print "Process takes %.2f seconds" % (time.time() - t0)
"""

#TEST2
"""
t0 = time.time()
myalg = MyBigradedAlgebra(["x", "y", "z"], [(6, 0), (0, 6), (3, -3)], [], True)
mymod = MyFreeBigradedModuleOverAlgebra(['e', 'f'], [(2, 4), (4, 2)], myalg)
actions = [ "z", "x*y", "y*z", "x*y*z" ]
process(mymod, actions, 'output.tex', 48, 24)
print "Process takes %.2f seconds" % (time.time() - t0)
"""

#TEST3

t0 = time.time()
myalg = MyBigradedAlgebra(["x", "y"], [(1, 0), (0, 1)], ["x^10=0", "x^8*y^2=0", "x^6*y^4=0", "x^4*y^6=0", "x^2*y^8=0", "y^10=0"], True)
mymod = MyFreeBigradedModuleOverAlgebra(['e', 'f'], [(12, 0), (0, 12)], myalg)
actions = [ "1", "x", "y", "x*y" ]
process(mymod, actions, 'output.tex', 24, 24)
print "Process takes %.2f seconds" % (time.time() - t0)
