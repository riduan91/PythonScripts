# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:16:02 2017

@author: ndoannguyen
"""

import numpy as np

INFTY = 1000

def simplifyListByReplacing(list1, list2):
    i = 0
    while (i < len(list1)):
        if list1[i : i + len(list2)] == list2:
            return []
    return list1
    
def reducedForm(increasing_list):
    if len(increasing_list) == 0:
        return []
    res = [(increasing_list[0], 1)]
    for u in increasing_list[1:] :
        if u == res[-1][0]:
            res[-1] = (res[-1][0], res[-1][1] + 1)
        else:
            res.append((u, 1))
    return res
    

class BigradedAlgebra:
    
    #--------------------INIT---------------------------------
    
    def __init__(self, nb_generators, bidegrees, relations, commutative=False):
        self.nb_generators = nb_generators
        self.bidegrees = np.array(bidegrees)
        self.relations = relations
        self.commutative = commutative

    
    #--------------------SIMPLIFY ELEMENTS--------------------    
    
    def simplifyTerm(self, term):
        # term is a pair (int, list)
        if term[0] == 0:
            return (0, [])
        if self.commutative:
            term = (term[0], sorted(term[1]))
        for relation in self.relations:
            if self.simplifyTermBySimpleRelation(term, relation)[0] == 0:
                return (0, [])
        else:
            return term
    
    def simplifyElement(self, element):
        #element is a list of term, like [ (3,[0,0,0,0,1,1]), (2,[1,1]), (-3, [0,0,0,0,1,1]), (-3,[1,1]), (1,[1,1]) ]
        for i, term in enumerate(element):
            element[i] = self.simplifyTerm(term)
        
        element = sorted(element, key = lambda x : x[1])
        simplified_element = [element[0]]
        for term in element[1:]:
            if term[1] == simplified_element[-1][1]:
                simplified_element[-1] = (simplified_element[-1][0] + term[0], term[1])
            else:
                simplified_element.append(term)
                
        for i, term in enumerate(simplified_element):
            simplified_element[i] = self.simplifyTerm(term)
            
        return self.simplifyZeroElement(simplified_element)
    
    def simplifyZeroElement(self, element):
        element = sorted(element, key = lambda x : x[1])
        if len(element) == 1 or element[0][0] != 0:
            return element
        else:
            return self.simplifyZeroElement(element[1:])

    def simplifyTermBySimpleRelation(self, term, relation):
        #relation is a list
        i = 0
        product = term[1]
        if self.commutative:
            if len(relation) == 1:
                isZero = True
                new_product = reducedForm(sorted(relation[0][1]))
                for occurence in new_product:
                    if "-".join(map(str, [occurence[0]] * occurence[1])) not in "-".join(map(str, product)):
                        isZero = False
            if isZero:
                return (0, [])
            else:
                return term
            
        for i in range (len(product)):
            if len(relation) == 1 and product[i : i + len(relation[0][1])] == relation[0][1]:
                return (0, [])
        return term

    
    #----------------COMPARE------------------------------------

    def isNullElement(self, element):
        element = self.simplifyElement(element)
        return element[0][0] == 0
    
    def areEqual(self, element1, element2):
        element1 = self.simplifyElement(element1)
        element2 = self.simplifyElement(element2)
        return self.isNullElement(self.substracElement(element1, element2))
    
    #----------------GET BIDEGREE-------------------------------
    
    def getBidegreeOfTerm(self, term):
        term = self.simplifyTerm(term)
        product = term[1]
        if term[0] == 0:
            return np.array([-INFTY, -INFTY])
        if product == []:
            return np.array([0, 0])
        s = sum( self.bidegrees[x] for x in product )
        return s
        
    def getBidegreeOfElement(self, element):
        element = self.simplifyElement(element)
        bidegree = self.getBidegreeOfTerm(element[0])
        for term in element[1:]:
            if list(self.getBidegreeOfTerm(term)) != list(bidegree):
                return None
        return bidegree
    
    #---------------ADDITION-------------------------------
    
    def addElement(self, element1, element2):
        element1 = self.simplifyElement(element1)
        element2 = self.simplifyElement(element2)
        return self.simplifyElement(element1 + element2)
        
    #--------------OPPOSITE---------------------------
    
    def getOpposite(self, element):
        element = self.simplifyElement(element)
        opposite_element = []
        for term in element:
            opposite_element.append((-term[0], term[1]))
        return opposite_element
    
    #---------------SUBSTRACTION-------------------------------
    
    def substractElement(self, element1, element2):
        element1 = self.simplifyElement(element1)
        element2 = self.simplifyElement(element2)
        return self.simplifyElement(self.addElement(element1, self.getOpposite(element2)))
    
    #--------------MULTIPLICATION---------------------
    
    def multiplyTerms(self, term1, term2):
        term1 = self.simplifyTerm(term1)
        term2 = self.simplifyTerm(term2)
        product1 = term1[1]
        product2 = term2[1]
        return self.simplifyTerm((term1[0] * term2[0], product1 + product2))
    
    def multiplyElements(self, element1, element2):
        element1 = self.simplifyElement(element1)
        element2 = self.simplifyElement(element2)
        res = []
        for term1 in element1:
            for term2 in element2:
                res.append(self.multiplyTerms(term1, term2))
        return self.simplifyElement(res)

    #----------EXPLORE ALL BIDEGREES---------------------
    
    def exploreTermsOfLimit(self, limit):
        return self.exploreTermsOfNbGeneratorsAndLimit(limit, self.nb_generators)
    
    def exploreTermsOfNbGeneratorsAndLimit(self, limit, nb_generators):
        if nb_generators <= 0:
            return [(1, [])]
        else:
            for ng in range(nb_generators):
                res = []
                preres = self.exploreTermsOfNbGeneratorsAndLimit(limit[:-1], nb_generators - 1)
                for term in preres:
                    for i in range(limit[-1] + 1):
                        new_term = self.simplifyTerm((term[0], term[1] + [nb_generators - 1] * i))
                        if new_term not in res:
                            res.append(new_term)
        return sorted(res, key = lambda x: len(x))
        
    def possibleBidegreesOfLimit(self, limit):
        allterms = self.exploreTermsOfLimit(limit)
        bidegrees = {}
        for term in allterms:
            bidegree = list(self.getBidegreeOfTerm(term))
            if str(bidegree) not in bidegrees:
                bidegrees[str(bidegree)] = [term]
            else:
                if term not in bidegrees[str(bidegree)]:
                    bidegrees[str(bidegree)].append(term)
        return bidegrees
    
    
    #--------------MULTIPLICATION ACTION----------------------
    
    def getConnectionsByAction(self, limit, element, side):
        source_bidegrees = self.possibleBidegreesOfLimit(limit)
        connections = []
        for k in source_bidegrees.keys():
            k_as_list = map(int, k[1:-1].split(", "))
            for V in source_bidegrees[k]:
                if side == 'left':
                    image = self.multiplyElements(element, [V])
                elif side == 'right':
                    image = self.multiplyElements([V], element)
                else:
                    return None
                if self.getBidegreeOfElement(image) is not None:
                    pair = (k_as_list, list(self.getBidegreeOfElement(image)))
                    if pair not in connections:
                        connections.append(pair)
        return sorted(connections)
    
    def getConnectionsByActionFromTheLeft(self, rank, term):
        return self.getConnectionsByAction(rank, term, 'left')
    
    def getConnectionsByActionFromTheRight(self, rank, term):
        return self.getConnectionsByAction(rank, term, 'right')
