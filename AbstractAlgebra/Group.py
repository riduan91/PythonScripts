# -*- coding: utf-8 -*-
"""
Created on Mon Jul 03 10:41:28 2017

@author: ndoannguyen
"""

from LocalFunctions import *

NEUTRAL_ELEMENT = "e"
EXPONENT_SIGN = "^"
MULTIPLICATION_SIGN = "*"
VARIABLE = "x"
END_OF_EQUATION = "=e"
ESPACE = " "
LEFT_BRACKET = "("
RIGHT_BRACKET = ")"

class GroupByGeneratorsAndRelations():
    
    def __init__(self, nb_generators, relation_expressions, commutative = False, nb_terms_in_simplest_form = -1):
        self.nb_terms_in_simplest_form = nb_generators
        if (nb_terms_in_simplest_form > 0):
            self.nb_terms_in_simplest_form = nb_terms_in_simplest_form
        self.nb_generators = nb_generators
        self.commutative = commutative
        if (self.nb_generators <= 1):
            self.commutative = True
        self.relations = []
        for relation_expression in relation_expressions:
            relation_expression = relation_expression.replace(ESPACE, "")
            if not relation_expression.endswith(END_OF_EQUATION):
                print "[Error] - Syntax error in relation_expression '%s': it must end with '= e'." % relation_expression
            else:
                try:
                    relation = []
                    terms = relation_expression.replace(END_OF_EQUATION, "").split(MULTIPLICATION_SIGN)
                    for term in terms:
                        #term is sth like (x1)^(-2) or x1
                        base, exponent = 0, 0
                        if term.find(EXPONENT_SIGN) >= 0:
                            term_pair = term.split(EXPONENT_SIGN)
                            base = int(term_pair[0].replace(LEFT_BRACKET, "").replace(RIGHT_BRACKET, "").replace(VARIABLE, ""))
                            exponent = int(term_pair[1].replace(LEFT_BRACKET, "").replace(LEFT_BRACKET, ""))
                            
                        else:
                            base = int(term.replace(LEFT_BRACKET, "").replace(LEFT_BRACKET, "").replace("x", ""))
                            exponent = 1
                        if exponent != 0:
                            relation.append((base, exponent)) 
                except:
                    print "[Error] - Syntax error in relation_expression '%s'" % relation_expression
                self.relations.append(relation)
        self.generalized_relations = []
        for i in range(self.nb_generators):
            # Firstly, relations of the form x * inverse(x) = e
            self.generalized_relations.append([i, self._index_of_inverse(i)])
            self.generalized_relations.append([self._index_of_inverse(i), i])
            
        relations_type_1 = []
        for relation in self.relations:
            #relation is sth like ([(0,1), (1,-1), (0,1)])            
            # Then, relations from self.relations               
            reformulated_relation = []
            for term in relation:
                #term is sth like (0,1)
                base, exponent = term[0], term[1]
                if exponent > 0:
                    reformulated_relation += [base] * exponent
                else:
                    reformulated_relation += [self._index_of_inverse(base)] * (-exponent)
            
            n = len(reformulated_relation)
            for permutator in range(n):
                permutated_relation = [reformulated_relation[(permutator + i) % n] for i in range(n)]
                relations_type_1.append(permutated_relation)      
            
            # Then, its inverse
            reformulated_relation = []
            for term in reversed(relation):
                #term is sth like (0,1)
                base, exponent = term[0], term[1]
                if exponent > 0:
                    reformulated_relation += [self._index_of_inverse(base)] * exponent
                else:
                    reformulated_relation += [base] * (-exponent)
            relations_type_1.append(reformulated_relation)
            
            n = len(reformulated_relation)
            for permutator in range(n):
                permutated_relation = [reformulated_relation[(permutator + i) % n] for i in range(n)]
                relations_type_1.append(permutated_relation)          
        
        relations_type_2 = relations_type_1
        relations_type_1 = sorted(relations_type_1, key = lambda x: len(x))
        
        for relation in relations_type_1:
            #print "-----Current relation-------", relation
            relation_sublists = sublists(relation)
            for sequence in relation_sublists:
                #print "---Current sequence---", sequence
                for other_relation in relations_type_1:
                    #print "Working with", other_relation
                    positions = all_discrete_positions_of_list_in_list(sequence, other_relation)
                    #print "Positions", positions
                    if len(positions) > 1:
                        for subset in all_subsets(positions):
                            if len(subset) > 0:
                                #print "Subset", subset
                                for position in subset:
                                    new_relation = other_relation[:position] + self._shortenSequenceInSpecifiedRelation(sequence, relation) + other_relation[position + len(sequence):]
                                    #print "New relation", new_relation                        
                                    if new_relation not in relations_type_2 and new_relation not in self.generalized_relations:
                                        relations_type_2.append(new_relation)

        self.generalized_relations += relations_type_2
    
    def description(self, style="simplified"):
        description = "This is a group of %d generator(s): " % self.nb_generators
        for i in range(self.nb_generators):
            description += "(x%d), " % i
        description += "\nwith the following relations: \n"
        for relation in self.relations:   
            description += "%s\n" % self._relationToExpression(relation)
        if self.commutative:
            description += "This group is declared as a commutative one.\n"
        else:
            description += "It may be not commutative.\n"
        if (style == "full"):
            description += "The relations can be reformulated as: \n"
            for relation in self.generalized_relations:
                description += "%s\n" % relation
        #Clean the description
        description = description.replace(",\n", "\n").replace(", \n", "\n")
        return description
    
    def _index_of_inverse(self, i):
        if i < self.nb_generators:
            return i + self.nb_generators
        else:
            return i - self.nb_generators
    
    def _simplify(self, element):
        element_sublists = sublists(element)
        transformed_element = element
        for sequence in element_sublists:
            transformed_sequence = self._shortenSequence(sequence)
            if transformed_sequence != sequence:
                position = position_of_list_in_list(sequence, element)
                transformed_element = element[:position] + transformed_sequence + element[position + len(sequence):]
                break
            
        if transformed_element != element:
            element = transformed_element
            return self._simplify(transformed_element)
            
        if len(element) <= self.nb_terms_in_simplest_form:
            return element
        
        for sequence in element_sublists:
            transformed_sequence = self._stronglyShortenSequence(sequence)
            if transformed_sequence != sequence:
                position = position_of_list_in_list(sequence, element)
                transformed_element = element[:position] + transformed_sequence + element[position + len(sequence):]
                break
        
        if transformed_element != element:
            element = transformed_element
            return self._simplify(transformed_element)
        
        return element
    
    def simplify(self, element):
        return self._elementToElementString(self._simplify(self.elementStringToElement(element)))
    
    def _multiply(self, element1, element2):
        return self._simplify(element1 + element2)
    
    def multiply(self, element1, element2):
        element1 = self.elementStringToElement(element1)
        element2 = self.elementStringToElement(element2)
        return 
        
    def _exponential(self, element, exponent):
        if exponent == 0:
            return []
        if exponent > 0:
            return self._simplify( self._multiply (self._exponential(element, exponent - 1), element ) )
        else:
            return self._simplify( self._multiply (self._exponential(element, exponent + 1), self._inverse(element) ) )

    def _isNeutral(self, element):
        return self._simplify(element) == []
        
    def _inverse(self, element):
        return [self._index_of_inverse(i) for i in reversed(element)]      
        
    def _areEqual(self, element1, element2):
        return self._isNeutral(element1 + self._inverse(element2))
            
    def _order(self, element):
        for i in range(1, 100):
            if self._isNeutral(self._exponential(element, i)):
                return i
        return "Unknown"            
    
    def _shortenSequence(self, sequence):
        """
            Sequence is the list form of an element
        """
        ordered_generalized_relations = sorted(self.generalized_relations, key = lambda x: len(x))
        transformed_sequence = sequence
        for relation in ordered_generalized_relations:
            #relation is sth like [0,1,2,2]
            if len(sequence) > len(relation)/2 and position_of_list_in_list(sequence, relation) >= 0:
                transformed_sequence = self._shortenSequenceInSpecifiedRelation(sequence, relation)
                break
        return transformed_sequence
    
    def _stronglyShortenSequence(self, sequence):
        """
            Sequence is the list form of an element
        """
        ordered_generalized_relations = sorted(self.generalized_relations, key = lambda x: len(x))
        transformed_sequence = sequence
        for relation in ordered_generalized_relations:
            #relation is sth like [0,1,2,2]
            if len(sequence) == len(relation)/2 and position_of_list_in_list(sequence, relation) >= 0:
                transformed_sequence = self._shortenSequenceInSpecifiedRelation(sequence, relation)
                break
        return transformed_sequence


    def _shortenSequenceInSpecifiedRelation(self, sequence, relation):
        """
            Sequence is the list form of an element
        """
        position = position_of_list_in_list(sequence, relation)
        remaining = remaining_of_list_after_removing(sequence, relation, position)
        transformed_sequence = self._inverse(remaining[0]) + self._inverse(remaining[1])
        return transformed_sequence
    
    def elementStringToElement(self, element_string):
        element_list = element_string.split(MULTIPLICATION_SIGN)
        element = []
        for term in element_list:
            term = term.replace(LEFT_BRACKET, "").replace(RIGHT_BRACKET, "")
            #term is sth like x0^3, 1
            if EXPONENT_SIGN in term:
                base, exponent = int(term.split(EXPONENT_SIGN)[0].replace(VARIABLE, "")), int(term.split(EXPONENT_SIGN)[1])
                if exponent > 0:
                    element += [base] * exponent
                else:
                    element += [self._index_of_inverse(base)] * (-exponent)
            else:
                element.append(int(term.replace(VARIABLE, "")))
        return element
    
    def _relationToExpression(self, relation):
        expression = ""
        for pair in relation:
            expression += "%s%d%s%d%s" % (VARIABLE, pair[0], EXPONENT_SIGN, pair[1], MULTIPLICATION_SIGN)
        expression += END_OF_EQUATION
        expression = expression.replace(MULTIPLICATION_SIGN + END_OF_EQUATION, END_OF_EQUATION)
        return expression
    
    def _elementToElementString(self, element):
        element_string = ""
        pairs = []
        if len(element) > 0:
            if element[0] < self.nb_generators:
                pairs.append([element[0], 1])
            else:
                pairs.append([self._index_of_inverse(element[0]), -1])
        for i in range(1, len(element)):
            if (element[i] == element[i-1] or self._index_of_inverse(element[i-1])) and element[i] < self.nb_generators:
                pairs[-1][1] += 1
            elif (element[i] == element[i-1] or self._index_of_inverse(element[i-1])) and element[i] >= self.nb_generators:
                pairs[-1][1] -= 1
            elif element[i] < self.nb_generators:
                pairs.append([element[i], 1])
            elif element[i] >= self.nb_generators:
                pairs.append([self._index_of_inverse(element[i]), -1])
        
        for pair in pairs:
            if pair[1] != 0:
                element_string += "%s%d%s%d%s" % (VARIABLE, pair[0], EXPONENT_SIGN, pair[1], MULTIPLICATION_SIGN)
        if element_string[-1] == MULTIPLICATION_SIGN:
            element_string = element_string[:-1]
        element_string = element_string.replace("%s1" % EXPONENT_SIGN, "")
        if element_string == "":
            element_string = NEUTRAL_ELEMENT
        return element_string


my_group = GroupByGeneratorsAndRelations(3, ["(x0)^2=e", "(x1)^2=e", "(x2)^3=e", "x0*x1*x2=e"], commutative = False)
#my_group = GroupByGeneratorsAndRelations(2, ["x0^4=e", "x0*x0*x1^-1*x1^-1=e", "x1*x0*x1^-1*x0=e"], False, 2)
#my_group = GroupByGeneratorsAndRelations(1, ["(x0)^7=e"], commutative=False)

print my_group.simplify("x1*x2^2*x0")