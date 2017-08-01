# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:29:15 2017

@author: ndoannguyen
"""

import numpy as np

class FreeBigradedModuleOverAlgebra:
    
    #--------------------INIT---------------------------------
    
    def __init__(self, nb_generators, bidegrees, algebra):
        self.nb_generators = nb_generators
        self.bidegrees = np.array(bidegrees)
        self.algebra = algebra
    
    #--------------------SIMPLIFICATION---------------------------------

    def simplifyTerm(self, term):
        # term is a pair (int, list)
        if self.algebra.isNullElement(self.algebra.simplifyElement(term[0])) or term[1] == -1:
            return ([(0, [])], -1)
        else:
            return (self.algebra.simplifyElement(term[0]), term[1])
    
    def simplifyVector(self, vector):
        #element is a list of term, like [ (3,[0,0,0,0,1,1]), (2,[1,1]), (-3, [0,0,0,0,1,1]), (-3,[1,1]), (1,[1,1]) ]
        vector = sorted(vector, key = lambda x : x[1])
        simplified_vector = [vector[0]]
        for term in vector[1:]:
            if term[1] == simplified_vector[-1][1]:
                simplified_vector[-1] = (self.algebra.addElement(simplified_vector[-1][0], term[0]), term[1])
            else:
                simplified_vector.append(term)
                
        for i, term in enumerate(simplified_vector):
            simplified_vector[i] = self.simplifyTerm(term)
            
        return self.simplifyZeroVector(simplified_vector)
        
    
    def simplifyZeroVector(self, vector):
        vector = sorted(vector, key = lambda x : x[1])
        if len(vector) == 1 or not self.algebra.isNullElement(vector[0][0]):
            return vector
        else:
            return self.simplifyZeroVector(vector[1:])
    
    #--------------------COMPARAISON-------------------------------------
    
    def isZeroVector(self, vector):
        vector = self.simplifyVector(vector)
        return vector[0][1] == -1
    
    def areEqual(self, vector1, vector2):
        vector1 = self.simplifyVector(vector1)
        vector2 = self.simplifyVector(vector2)
        return self.isZeroVector(self.substractVector(vector1, vector2))
        
    #--------------------ACTION/OPPOSITE/SUBSTRACTION--------------------------
    
    def addVector(self, vector1, vector2):
        vector1 = self.simplifyVector(vector1)
        vector2 = self.simplifyVector(vector2)
        return self.simplifyVector(vector1 + vector2)   
    
    def getOppositeVector(self, vector):
        vector = self.simplifyVector(vector)
        opposite_vector = []
        for term in vector:
            opposite_vector.append((self.algebra.getOpposite(term[0]), term[1]))
        return opposite_vector

    def substractVector(self, vector1, vector2):
        vector1 = self.simplifyVector(vector1)
        vector2 = self.simplifyVector(vector2)
        return self.simplifyVector(self.addVector(vector1, self.getOppositeVector(vector2)))  

    #--------------------MULTIPLICATION-----------------------------------
                     
    def multiplicationByScalar(self, element, vector):
        vector = self.simplifyVector(vector)
        newvector = []
        for term in vector:
            newvector.append((self.algebra.multiplyElements(element, term[0]) , term[1]))
        newvector = self.simplifyVector(newvector)
        return newvector
    
    #--------------------GET BIDEGREE-----------------------------------
    
    def getBidegreeOfTerm(self, term):
        term = self.simplifyTerm(term)
        if term[1] == -1:
            return np.array([-1000, -1000])
        return self.bidegrees[term[1]] + self.algebra.getBidegreeOfElement(term[0])
    
    def getBidegreeOfVector(self, vector):
        vector = self.simplifyVector(vector)
        bidegree = self.getBidegreeOfTerm(vector[0])
        for term in vector[1:]:
            if list(self.getBidegreeOfTerm(term)) != list(bidegree):
                return None
        return bidegree
    
    #--------------------EXPLORE ALL DEGREE-----------------------------
        
    def possibleTermsOfRankNoGreaterThan(self, rankofelement):
        terms = self.algebra.possibleTermsOfRankNoGreaterThan(rankofelement)
        res = []
        for v in range(self.nb_generators):
            for term in terms:
                new_term = self.simplifyTerm(([term], v))
                if new_term not in res:
                    res.append(new_term)
        return res
    
    def possibleTermsOfRankNoGreaterThanWithLimit(self, rankofelement, lim):
        terms = self.algebra.possibleTermsOfRankNoGreaterThanWithLimit(rankofelement, lim)
        res = []
        for v in range(self.nb_generators):
            for term in terms:
                new_term = self.simplifyTerm(([term], v))
                if new_term not in res:
                    res.append(new_term)
        return res
    
        
    def possibleTermsOfLimit(self, lim):
        terms = self.algebra.exploreTermsOfLimit(lim)
        res = []
        for v in range(self.nb_generators):
            for term in terms:
                new_term = self.simplifyTerm(([term], v))
                if new_term not in res:
                    res.append(new_term)
        return res
    
    def possibleBidegreesOfRankNoGreaterThan(self, rankofelement):
        terms = self.possibleTermsOfRankNoGreaterThan(rankofelement)
        bidegrees = {}
        for term in terms:
            bidegree = list(self.getBidegreeOfTerm(term))
            if str(bidegree) not in bidegrees:
                bidegrees[str(bidegree)] = [term]
            else:
                bidegrees[str(bidegree)].append(term)
        return bidegrees
        
    def possibleBidegreesOfRankNoGreaterThanWithLimit(self, rankofelement, lim):
        terms = self.possibleTermsOfRankNoGreaterThanWithLimit(rankofelement, lim)
        bidegrees = {}
        for term in terms:
            bidegree = list(self.getBidegreeOfTerm(term))
            if str(bidegree) not in bidegrees:
                bidegrees[str(bidegree)] = [term]
            else:
                if term not in bidegrees[str(bidegree)]:
                    bidegrees[str(bidegree)].append(term)
        return bidegrees
        
    def possibleBidegreesOfLimit(self, lim):
        terms = self.possibleTermsOfLimit(lim)
        bidegrees = {}
        for term in terms:
            bidegree = list(self.getBidegreeOfTerm(term))
            if str(bidegree) not in bidegrees:
                bidegrees[str(bidegree)] = [term]
            else:
                if term not in bidegrees[str(bidegree)]:
                    bidegrees[str(bidegree)].append(term)
        return bidegrees
    
    
    #--------------------GET CONNECTIONS AFTER ACTION-------------------
    
    def getConnectionsByAction(self, source_bidegrees, rank, element):
        if self.algebra.getBidegreeOfElement(element) is None:
            print "Unknown bidegree."
            return None
        
        connections = []
        for k in source_bidegrees.keys():
            k_as_list = map(int, k[1:-1].split(", "))
            for V in source_bidegrees[k]:
                image = self.multiplicationByScalar(element, [V])
                pair = (k_as_list, list(self.getBidegreeOfVector(image)))
                if pair not in connections:
                    connections.append(pair)
        return sorted(connections)
    
    def getConnectionsByActionWithLimit(self, source_bidegrees, element, lim = None):
        if lim is None:
            return self.getConnectionsByActionWithLimit(source_bidegrees, element, 10)
        
        connections = []
        for k in source_bidegrees.keys():
            k_as_list = map(int, k[1:-1].split(", "))
            if abs(k_as_list[0]) + abs(k_as_list[1]) <= lim:
                for V in source_bidegrees[k]:
                    image = self.multiplicationByScalar(element, [V])
                    b = self.getBidegreeOfVector(image)
                    if abs(b[0]) + abs(b[1]) <= lim:
                        pair = (k_as_list, list(self.getBidegreeOfVector(image)))
                        if pair not in connections:
                            connections.append(pair)
                    else:
                        pair = (k_as_list, [-999, -999])
                        if pair not in connections:
                            connections.append(pair)
        return sorted(connections)

