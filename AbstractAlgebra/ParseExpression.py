# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:18:18 2017

@author: ndoannguyen
"""

from BigradedAlgebra import BigradedAlgebra
from BigradedModule import FreeBigradedModuleOverAlgebra

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class MyBigradedAlgebra:
    
    def __init__(self, variables, bidegrees, relation_strings, commutative=False):
        self.variables = variables
        self.variable_dictionary = {}
        
        for idx, variable in enumerate(variables):
            self.variable_dictionary[variable] = idx
        
        self.relation_strings = relation_strings
        
        relations = []
        for rel_string in relation_strings:
            r = self.parseRelationString(rel_string)
            if r is not None:
                relations.append(r)            
            
        self.alg = BigradedAlgebra(len(variables), bidegrees, relations, commutative)
        
        
    #----------------------PARSE STRING TO ELEMENTS---------------------------------
        
    def parseRelationString(self, rel_string):
        rel_string = rel_string.replace(" ", "")
        if not rel_string.endswith("=0"):
            print "[Error] Relations must end with '= 0'"
            return None
        rel_string = rel_string.replace("=0", "")

        return self.parseElementString(rel_string)
        
    def parseElementString(self, ele_string):
        
        ele_string = ele_string.replace(" ", "")   
                
        if '(' in ele_string or ')' in ele_string or '[' in ele_string or ']' in ele_string:
            print "[Error] Please rewrite the expression without using parentheses."
            return None
        
        if ele_string[0] != '+' and ele_string[0] != '-':
            ele_string = '+' + ele_string

        result = []            
        
        terms = []
        current_pos = 0
        current_term = ''
        while current_pos < len(ele_string):
            current_char = ele_string[current_pos]
            if current_char != '+' and current_char != '-':
                current_term += current_char
            else:
                if len(current_term) > 0:
                    terms.append(current_term)
                current_term = current_char
            current_pos += 1
        
        if len(current_term) > 0:
            terms.append(current_term)
            
        for term in terms:
            new_term = self.parseTerm(term)
            if new_term[0] != 0:
                result.append((new_term[0], new_term[1]))
        
        if result == []:
            result = [(0, [])]
        return result
    
    def parseTerm(self, term):
        new_term = [0, []]
        S = term.split("*")
        for s in S:
            if '^' not in s:
                if RepresentsInt(s):
                    s = int(s)
                    new_term[0] = s
                elif s[0] == '+' and self.variable_dictionary.has_key(s[1:]):
                    new_term[0] = 1
                    new_term[1] = [self.variable_dictionary[s[1:]]]
                elif s[0] == '-' and self.variable_dictionary.has_key(s[1:]):
                    new_term[0] = -1
                    new_term[1] = [self.variable_dictionary[s[1:]]]
                elif self.variable_dictionary.has_key(s):
                    new_term[1].append(self.variable_dictionary[s])
            else:
                R = s.split("^")
                if not RepresentsInt(R[1]):
                    break
                else:
                    exponent = int(R[1])
                    left_part = R[0]
                    if left_part[0] == '+' and self.variable_dictionary.has_key(left_part[1:]):
                        new_term[0] = 1
                        new_term[1] = [self.variable_dictionary[left_part[1:]]] * exponent
                    elif left_part[0] == '-' and self.variable_dictionary.has_key(left_part[1:]):
                        new_term[0] = -1
                        new_term[1] = [self.variable_dictionary[left_part[1:]]] * exponent
                    elif self.variable_dictionary.has_key(left_part):
                        new_term[1] += [self.variable_dictionary[left_part]] * exponent
        return (new_term[0], new_term[1])
    
    #----------------------ElEMENT TO STRING-----------------------------
        
    def stringifyElement(self, element):
        if self.alg.isNullElement(element):
            return '0'
        else:
            res = "+".join([ str(term[0]) + "*" + "*".join([ self.variables[x[0]] + "^" + str(x[1]) for x in self.stringifyList(term[1])]) for term in element])                      
            res = res.replace("**", "*").replace("*+", "+").replace("*-", "-").replace("^1", "")
            if res != "1*":
                res = res.replace("1*", "")
            else:
                res = res.replace("1*", "1")
            res = res.replace("+-", "-")
            return res
    
    def stringifyList(self, mylist):
        if mylist == []:
            return []
        newlist = [[mylist[0], 1]]
        for variable in mylist[1:]:
            if variable == newlist[-1][0]:
                newlist[-1][1] += 1
            else:
                newlist += [[variable, 1]]
        return newlist
        
    #---------------------SIMPLIFICATION-----------------------------------
    
    def simplify(self, element):
        element = self.parseElementString(element)
        return self.stringifyElement( self.alg.simplifyElement(element) )
        
    #---------------------COMPARAISON-----------------------------------
    
    def isNull(self, element):
        element = self.parseElementString(element)
        return self.alg.isNullElement(element)
    
    def areEqual(self, element1, element2):
        element1 = self.parseElementString(element1)
        element2 = self.parseElementString(element2)
        return self.alg.areEqual(element1, element2)
        
    #---------------------GET BIDEGREE-------------------------------------
        
    def getBidegree(self, element):
        element = self.parseElementString(element)
        return self.alg.getBidegreeOfElement(element)
    
    #--------------------------ADDITION-------------------------------
    
    def add(self, element1, element2):
        element1 = self.parseElementString(element1)
        element2 = self.parseElementString(element2)
        return self.stringifyElement(self.alg.addElement(element1, element2))
    
    def opposite(self, element):
        element = self.parseElementString(element)
        return self.stringifyElement(self.alg.getOpposite(element))
    
    def substract(self, element1, element2):
        element1 = self.parseElementString(element1)
        element2 = self.parseElementString(element2)
        return self.stringifyElement(self.alg.substractElement(element1, element2))
        
    #--------------MULTIPLICATION---------------------
        
    def multiply(self, element1, element2):
        element1 = self.parseElementString(element1)
        element2 = self.parseElementString(element2)
        return self.stringifyElement(self.alg.multiplyElements(element1, element2))
    
    #----------EXPLORE ALL BIDEGREES---------------------
    
    def findBidegreesOfRankNoGreaterThan(self, rank):
        bidegrees = self.alg.possibleBidegreesOfRankNoGreaterThan(rank)
        for (k, V) in bidegrees.items():
            new_V = []
            for v in V:
                new_V.append(self.stringifyElement([v]))
            bidegrees[k] = new_V 
        return bidegrees
    
    def findBidegreesOfLimit(self, limit):
        bidegrees = self.alg.possibleBidegreesOfLimit(limit)
        for (k, V) in bidegrees.items():
            new_V = []
            for v in V:
                new_V.append(self.stringifyElement([v]))
            bidegrees[k] = new_V 
        return bidegrees
    
    def findConnectionsByActionFromTheLeft(self, rank, element):
        element = self.parseElementString(element)
        return self.alg.getConnectionsByActionFromTheLeft(rank, element)
    
    def findConnectionsByActionFromTheRight(self, rank, element):
        element = self.parseElementString(element)
        return self.alg.getConnectionsByActionFromTheRight(rank, element)

#----------------------------------------------------------------------------------------------------------



class MyFreeBigradedModuleOverAlgebra:
    
    def __init__(self, variables, bidegrees, myalg):
        self.variables = variables
        self.variable_dictionary = {}
        
        for idx, variable in enumerate(variables):
            self.variable_dictionary[variable] = idx        
            
        self.mod = FreeBigradedModuleOverAlgebra( len(variables), bidegrees, myalg.alg )
        self.myalg = myalg
        
    #----------------------PARSE STRING TO VECTORS---------------------------------
        
    def parseVectorString(self, vector_string):
        if vector_string == '0':
            vector_string = "(0)*" + self.variables[0]
        
        vector_string = vector_string.replace(" ", "")   
        vector_string = vector_string.replace("-(-", "+(").replace("-(+", "-(").replace("+(-", "-(").replace("+(+", "+(").replace("(-", "-(").replace("(+", "+(")
        
        if '[' in vector_string or ']' in vector_string:
            print "[Error] Please don't use '[' nor ']'."
            return None
        if vector_string[0] != '+' and vector_string[0] != '-':
            vector_string = '+' + vector_string

        result = []            
        
        terms = []
        current_pos = 0
        current_term = ''
        inside = 0
        while current_pos < len(vector_string):
            current_char = vector_string[current_pos]
            if current_char == '(':
                inside += 1
            if current_char == ')':
                inside -= 1
            if inside > 0 or (current_char != '+' and current_char != '-'):
                current_term += current_char
            else:
                if len(current_term) > 0:
                    terms.append(current_term)
                current_term = current_char
            current_pos += 1
        
        if len(current_term) > 0:
            terms.append(current_term)
            
        for term in terms:
            term = term.replace("+(", "(+").replace("-(", "(-")
            if term[0]!="(" or term[-3]!=")" or term[-2]!="*":
                continue
            ele_string = term[1:-3]
            generator_string = term[-1]
            result.append((self.myalg.parseElementString(ele_string), self.variable_dictionary[generator_string]))
        
        return self.mod.simplifyVector(result)
    
    #----------------------STRING TO VECTOR-----------------------------
    
    def stringifyVector(self, vector):
        substrings = []
        for term in vector:
            substrings.append( "(" + self.myalg.stringifyElement(term[0]) + ")*" + self.variables[term[1]] )
        res = "+".join(substrings).replace("+(-", "-(").replace("(-", "-(")
        if res == "(0)*" + self.variables[-1]:
            res = "0"
        return res
    
    #--------------------SIMPLIFICATION---------------------------------

    def simplify(self, vector):
        vector = self.parseVectorString(vector)
        return self.stringifyVector(self.mod.simplifyVector(vector))
    
    #--------------------COMPARAISON---------------------------------
    
    def isNull(self, vector):
        vector = self.parseVectorString(vector)
        return self.mod.isZeroVector(vector)   
    
    def areEqual(self, vector1, vector2):
        vector1 = self.parseVectorString(vector1)
        vector2 = self.parseVectorString(vector2)
        return self.mod.areEqual(vector1, vector2)
    
    #--------------------ACTION/OPPOSITE/SUBSTRACTION--------------------------
    
    def add(self, vector1, vector2):
        vector1 = self.parseVectorString(vector1)
        vector2 = self.parseVectorString(vector2)
        return self.stringifyVector(self.mod.addVector(vector1, vector2))
    
    def opposite(self, vector):
        vector = self.parseVectorString(vector)
        return self.stringifyVector(self.mod.getOppositeVector(vector))
    
    def substract(self, vector1, vector2):
        vector1 = self.parseVectorString(vector1)
        vector2 = self.parseVectorString(vector2)
        return self.stringifyVector(self.mod.substractVector(vector1, vector2))
        
    #--------------------MULTIPLICATION-----------------------------------
        
    def multiplyByScalar(self, scalar, vector):
        vector = self.parseVectorString(vector)
        scalar = self.myalg.parseElementString(scalar)
        return self.stringifyVector(self.mod.multiplicationByScalar(scalar, vector))
        
    #--------------------GET BIDEGREE-------------------------------------
        
    def getBidegree(self, vector):
        vector = self.parseVectorString(vector)
        return self.mod.getBidegreeOfVector(vector)
    
    #--------------------EXPLORE ALL DEGREE-----------------------------
    
    def findBidegreesOfRankNoGreaterThan(self, rank):
        bidegrees = self.mod.possibleBidegreesOfRankNoGreaterThan(rank)
        for (k, V) in bidegrees.items():
            new_V = []
            for v in V:
                new_V.append(self.stringifyVector([v]))
            bidegrees[k] = new_V 
        return bidegrees    
    
    def findConnectionsByAction(self, source_bidegrees, rank, element='1'):
        element = self.myalg.parseElementString(element)
        return self.mod.getConnectionsByAction(source_bidegrees, rank, element)

    def findConnectionsByActionWithLimit(self, source_bidegrees, element='1', lim = None):
        element = self.myalg.parseElementString(element)
        return self.mod.getConnectionsByActionWithLimit(source_bidegrees, element, lim)
