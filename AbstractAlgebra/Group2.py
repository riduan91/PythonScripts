# -*- coding: utf-8 -*-
"""
Created on Sat Jul 08 15:34:29 2017

@author: ndoannguyen
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 03 10:41:28 2017

@author: ndoannguyen
"""

from LocalFunctions import position_of_list_in_list, all_discrete_positions_of_list_in_list, remaining_of_list_after_removing, sublists, all_subsets, to_string
import re, copy, time

NEUTRAL_ELEMENT = "e"
EXPONENT_SIGN = "^"
MULTIPLICATION_SIGN = "*"
VARIABLE = "x"
END_OF_EQUATION = "=e"
ESPACE = " "
LEFT_BRACKET = "("
RIGHT_BRACKET = ")"

class GroupByGeneratorsAndRelations():
    
    def __init__(self, name, nb_generators, relation_expressions, commutative = False, nb_terms_in_simplest_form = -1):
        """
            Form the group from name, number of generators, relations, information about commutativity and maximum number of terms in the simplest form of an element of group
        """
        #Define the name
        self.name = name
        
        #Define the number of generators                
        self.nb_generators = nb_generators

        #Suppose that every element of this group can be represented as the product of no more than some number of generators and their inverse
        self.nb_terms_in_simplest_form = nb_generators        
        if (nb_terms_in_simplest_form > 0):
            self.nb_terms_in_simplest_form = nb_terms_in_simplest_form
        
        #By default, the group is not commutative if there are 2 or more generators. 
        self.commutative = commutative
        if (self.nb_generators <= 1):
            self.commutative = True
        
        #Attention: self.generators is a dictionary of generators and the neutral element also
        self.generators = {"e": "e"}
        
        #All elements
        self.all_elements = []
        
        #A relation is a list like [1, 2, 3, 4]. By default, self.relations is empty
        self.relations = []

        #We parse the relations under the form of expression to list form 
        for relation_expression in relation_expressions:
            # Retrieve all different variables to the dictionary self.generators, which is sth like {x: x1, y:x2, z:x3, e:e}
            relation_expression = self.retrieveVariablesFromExpression(relation_expression)
            
            relation_expression = relation_expression.replace(ESPACE, "")

            if not relation_expression.endswith(END_OF_EQUATION):
                print "[Error] - Syntax error in relation_expression '%s': it must end with '= e'." % relation_expression
 
            else:
                try:
                    relation = []
                    # Split the expression without "=e" using separator "*", terms will be sth like [(x1)^(-2), x1]
                    terms = relation_expression.replace(END_OF_EQUATION, "").split(MULTIPLICATION_SIGN)
                    for term in terms:
                        #term is sth like (x1)^(-2) or x2
                        base, exponent = 0, 0
                        if term.find(EXPONENT_SIGN) >= 0:
                            term_pair = term.split(EXPONENT_SIGN)
                            #term_pair is sth like (x1), (-2)
                            base = int(term_pair[0].replace(LEFT_BRACKET, "").replace(RIGHT_BRACKET, "").replace(VARIABLE, ""))
                            #In this example, base is 1
                            exponent = int(term_pair[1].replace(LEFT_BRACKET, "").replace(LEFT_BRACKET, ""))
                            #And exponent is -2
                        else:
                            #Here term is sth like x2
                            base = int(term.replace(LEFT_BRACKET, "").replace(LEFT_BRACKET, "").replace("x", ""))
                            #In this example, base is 2, after removing x
                            exponent = 1
                            #And exponent is 1
                        if exponent != 0:
                            relation.append((base, exponent)) 
                    #After the loop, relation is sth like [(1,-2), (2,1)]
                except:
                    print "[Error] - Syntax error in relation_expression '%s'" % relation_expression
                self.relations.append(relation)
                #After this loop, relations is sth like [[(1,-2), (2,1)], [(1,4)]]
        
        for relation in self.relations:
            if len(relation) == 2:
                x, exponent_x, y, exponent_y = relation[0][0], relation[0][1], relation[1][0], relation[1][1]
                for another_relation in self.relations:
                    new_relation = []
                    if len(another_relation) == 1 and another_relation[0][0] == x and abs(exponent_y) * another_relation[0][1] % abs(exponent_x) == 0:
                        new_relation = [(y, abs(exponent_y) * another_relation[0][1] / abs(exponent_x))]
                    elif len(another_relation) == 1 and another_relation[0][0] == y and abs(exponent_y) * another_relation[0][1] % abs(exponent_y) == 0:
                        new_relation = [(x, abs(exponent_x) * another_relation[0][1] / abs(exponent_y))]
                    if len(new_relation) and new_relation not in self.relations:
                        self.relations.append(new_relation)
                
        #We want to facilitate the substitution in element simplification later, so we try to generate as many relations as possible
        #That's why we define self.generalized relations here.
              
        self.equality_classes = []
        self.to_class = {}
        self.generalized_relations = []
        self._generalizeRelations()
        
        
        #Store the variables in another way, {x1:x, x2:y, x3:z, e:e} instead of {x:x1, y:x2, z:x3, e:e}
        self.reversed_generators = {}
        for generator in self.generators.keys():
            self.reversed_generators[self.generators[generator]] = generator
        
        self.commutative = self._checkCommutative()
        

        self.all_elements = self._listAllElements()
        self.all_elements_as_string = [self._elementToElementString(element) for element in self.all_elements]
        
        self.order = len(self.all_elements)
        self.multiplication_table = self._createMultiplicationTable()
        self.multiplication_table_as_string = self.createMultiplicationTable()
        
        print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        print self.description()
        

    def _generalizeRelations(self):
        for i in range(1, self.nb_generators + 1):
            # Firstly, find all relations of the form x * inverse(x) = e
            self.generalized_relations.append([i, self._index_of_inverse(i)])
            self.generalized_relations.append([self._index_of_inverse(i), i]) 
        
        #Now, generate all relations that is a permutation of relations in self.relations, for example [1,2,3] will be [1,2,3], [2,3,1] and [3,1,2]
        #We call them relation of type 1
        
        relations_type_1 = []
        for relation in self.relations:
            # Here relation is sth like ([(1,1), (2,-1), (3,1)])                       
            reformulated_relation = []
            for term in relation:
                #term is sth like (1,1)
                base, exponent = term[0], term[1]
                if exponent > 0:
                    reformulated_relation += [base] * exponent
                else:
                    reformulated_relation += [self._index_of_inverse(base)] * (-exponent)
                #After this step, our example become [1,5,3]
            
            n = len(reformulated_relation)
            for permutator in range(n):
                permutated_relation = [reformulated_relation[(permutator + i) % n] for i in range(n)]
                if permutated_relation not in relations_type_1:
                    relations_type_1.append(permutated_relation)
            #After this step, relations_type_1 contains [1,5,3], [5,3,1], [3,1,5]
            
            #We also express the inverse form of the relation. E.g, [1,5,3] becomes [6,2,4]
            #Do the same, we get more elements of relations_type_1: [6,2,4], [2,4,6], [4,6,2]
            reformulated_relation = []
            for term in reversed(relation):
                #term is sth like (0,1)
                base, exponent = term[0], term[1]
                if exponent > 0:
                    reformulated_relation += [self._index_of_inverse(base)] * exponent
                else:
                    reformulated_relation += [base] * (-exponent)
            
            n = len(reformulated_relation)
            for permutator in range(n):
                permutated_relation = [reformulated_relation[(permutator + i) % n] for i in range(n)]
                if permutated_relation not in relations_type_1:
                    relations_type_1.append(permutated_relation)          
        
        #We want to define relations of type 2, which is formed by mean of: find another form of some sequence form a relation, then replace it in another relation
        #For example, if x1*x1=e, we have [1,1]=[] or equivalently, [1]=[4], hence in [1,5,3], we can substitute [1] in this relation and it becomes [4,5,3]
        
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
                                    #print "Use %s in position %d in %s, %s becomes %s"% (sequence, position, relation, other_relation, new_relation)
                                    #print "New relation", new_relation                        
                                    if new_relation not in relations_type_2 and new_relation not in self.generalized_relations:
                                        relations_type_2.append(new_relation)
       
        self.generalized_relations += relations_type_2   

        relations_type_3 = []
        for relation in self.relations:
            if len(relation) == 1 and relation[0][1] == 2:
                x = relation[0][0]
                y = self._index_of_inverse(x)
                for another_relation in self.generalized_relations:
                    new_another_relation = copy.copy(another_relation)
                    for idx in range(len(another_relation)):
                        if another_relation[idx] == x:
                            new_another_relation[idx] = y
                        if another_relation[idx] == y:
                            new_another_relation[idx] = x
                    if new_another_relation not in self.generalized_relations and new_another_relation not in relations_type_3:
                        relations_type_3.append(new_another_relation)
        self.generalized_relations += relations_type_3        
        
        self.to_class[to_string([])] = 0
        self.equality_classes.append([])
        self.equality_classes[0].append([])
    
        for relation in self.generalized_relations:
            
            for i in range(len(reformulated_relation), -1, -1):
                for j in range (0, len(reformulated_relation) - i):
                    sequence = reformulated_relation[j : j + i + 1]
                    remaining = remaining_of_list_after_removing(sequence, reformulated_relation, j)
                    transformed_sequence = self._inverse(remaining[0]) + self._inverse(remaining[1])
                    if to_string(sequence) not in self.to_class.keys():
                        if to_string(transformed_sequence) not in self.to_class.keys():
                            self.create_new_class(transformed_sequence)               
                        self.join_class(sequence, transformed_sequence)
                    else:
                        if to_string(transformed_sequence) not in self.to_class.keys():
                            self.join_class(transformed_sequence, sequence)
                        else:
                            self.update_equalitiy_classes(transformed_sequence, sequence)
    
    def create_new_class(self, element):
         self.to_class[to_string(element)] = len(self.equality_classes)
         self.equality_classes.append([element])       

    def join_class(self, element, another_element):
        self.to_class[to_string(element)] = self.to_class[to_string(another_element)]
        self.equality_classes[self.to_class[to_string(another_element)]].append(element)
        self.equality_classes[self.to_class[to_string(another_element)]] = sorted(self.equality_classes[self.to_class[to_string(another_element)]], key = lambda x: (len(x), str(x)))
    
    def update_equalitiy_classes(self, element, another_element):
        m1, m2 = self.to_class[to_string(element)], self.to_class[to_string(another_element)], 
        if m1 != m2:
            m = min(m1, m2)
            M = max(m1, m2)
            for element in self.equality_classes[M]:
                self.to_class[to_string(element)] = m
            self.equality_classes[m] += self.equality_classes[M]
            self.equality_classes[M] = []
            self.equality_classes[m] = sorted(self.equality_classes[m], key = lambda x: (len(x), str(x)))

    
    def description(self, style="simplified"):
        """
            Describe the group
        """
        
        if self.name != None:
            description = "The group %s is generated by " % self.name
        else:
            description = "This is a group generated by "

        description += "%d generator(s): " % self.nb_generators

        for i in range(1, self.nb_generators + 1):
            description += "%s, " % self.reversed_generators[VARIABLE + str(i)]
        description += "\nand the following relations: \n"

        for relation in self.relations:   
            description += "%s\n" % self._relationToExpression(relation)

        if (style == "full"):
            description += "The relations can be reformulated as: \n"
            for relation in self.generalized_relations:
                description += "%s\n" % relation
 
        description += "It is of order %d with the elements: %s.\n" % (self.order, ", ".join([self._elementToElementString(element) for element in self.all_elements]))
        
        description += "Multiplication table: \n"
        space = max([len(element) for element in self.all_elements_as_string]) + 2
        
        description += "%*s" % (space, 'x') + "".join(["%*s" % (space, element) for element in self.all_elements_as_string]) + "\n"
        for idx in range(self.order):
            description += "%*s" % (space, self.all_elements_as_string[idx]) + "".join(["%*s" % (space, element) for element in self.multiplication_table_as_string[idx]]) + "\n"

        description = description.replace(",\n", "\n").replace(", \n", "\n")
        return description
    
    def _index_of_inverse(self, index_of_generator):
        """
            If there are n generators, they will be called x1, x2, ..., xn and there inverse will be called x(n+1), ..., x(2n)
        """
        if index_of_generator <= self.nb_generators:
            return index_of_generator + self.nb_generators
        else:
            return index_of_generator - self.nb_generators 
    
    def _getClass(self, element):
        return self.equality_classes[self.to_class[to_string(element)]]
    
    def _simplify(self, element):
        print "element", element
        if to_string(element) in self.to_class.keys():
            return self._getClass(element)[0]
        
        if len(element) <= self.nb_terms_in_simplest_form:
            self.create_new_class(element)
            return element
           
        transformed_element = copy.copy(element)
        for i in range(len(transformed_element), -1, -1):        
            for j in range (0, len(transformed_element) - i):
                sequence = transformed_element[j : j + i + 1]
                print "sequence", sequence
                if to_string(sequence) not in self.to_class.keys():
                    continue
        
                for replacement in self._getClass(sequence):
                    if len(replacement) > len(sequence):
                        continue
                
                    transformed_element = element[:j] + replacement + element[j + i + 1:]
                    print "transformed_element", transformed_element
                
                    simplified_transformed_element = self._simplify(transformed_element)
                    print simplified_transformed_element
                
                    if simplified_transformed_element in self.to_class.keys():
                        self.join_class(element, simplified_transformed_element)
                        return self._getClass(simplified_transformed_element)[0]
                        
            return element
    
    def simplify(self, element):
        """
            Find the simplest form of an element. For example, for the group of 1 generator x1 and 1 relation x1^5=0, x1^4 will return x1^-1
            This works with element in string form.
        """
        if len(self.all_elements) > 0:
            return self._elementToElementString(self._strongSimplify(self.elementStringToElement(element)))
        return self._elementToElementString(self._simplify(self.elementStringToElement(element)))
    
    def _multiply(self, element1, element2):
        """
            Multiply to 2 elements of the group in list form. E.g, for the group of 1 generator x1 and 1 relation x1^5=0, multiplying [1,1,1] and [1,1] returns [].
            This works with elements in list form.
        """
        return self._simplify(element1 + element2)
    
    def multiply(self, element1, element2):
        """
            Multiply to 2 elements of the group in list form. E.g, for the group of 1 generator x1 and 1 relation x1^5=0, multiplying x1^3 and x1^2 returns e.
            This works with elements in string form.
        """
        return self._elementToElementString(self._multiply(self._simplify(self.elementStringToElement(element1)), self._simplify(self.elementStringToElement(element2))))
        
    def _power(self, element, exponent):
        """
            Return element to a power in group. For example, for the group of 1 generator x1 and 1 relation x1^5=0, _power(1,4) returns [3].
            This works with elements in list form.
        """
        if self.order > 0:
            exponent = exponent % self.order
        if exponent == 0:
            return []
        return self._simplify( self._multiply (self._power(element, exponent - 1), element ) )
    
    def power(self, element, exponent):
        """
            Return element to a power in group. For example, for the group of 1 generator x1 and 1 relation x1^5=0, power('x1',4) returns x1^-1.
            This works with elements in list form.
        """
        return self._elementToElementString(self._exponential(self.elementStringToElement(element), exponent))

    def _isNeutral(self, element):
        """
            Check if an element (in list form) is neutral.
        """
        return self._simplify(element) == []
    
    def isNeutral(self, element):
        """
            Check if an element (in string form) is neutral.
        """
        return self._isNeutral(self.elementStringToElement(element))
        
    def _inverse(self, element):
        """
            Return the inverse of an element (in list form).
        """
        return [self._index_of_inverse(i) for i in reversed(element)]      
        
    def _areEqual(self, element1, element2):
        """
            Return the inverse of an element (in string form).
        """
        return self._isNeutral(element1 + self._inverse(element2))
            
    def _order(self, element):
        """
            Return the order of an element (in list form) in the group
        """
        if self.order > 0:
            for i in range(1, self.order + 1):
                if self._isNeutral(self._power(element, i)):
                    return i
        return "Unknown" 

    def order(self, element):
        """
            Return the order of an element (in string form) in the group
        """
        return self._order(self.elementStringToElement(element))           
    
    def _shortenSequence(self, sequence):
        """
            Sequence is the list form of an element
        """
        ordered_generalized_relations = sorted(self.generalized_relations, key = lambda x: len(x))
        transformed_sequence = sequence
        for relation in ordered_generalized_relations:
            #relation is sth like [0,1,2,2]
            if len(sequence) > len(relation)/2  and position_of_list_in_list(sequence, relation) >= 0:
                transformed_sequence = self._shortenSequenceInSpecifiedRelation(sequence, relation)
                break
        return transformed_sequence
    
    def _shortenSequenceWithAlgo2(self, sequence):
        """
            Sequence is the list form of an element
        """
        ordered_generalized_relations = sorted(self.generalized_relations, key = lambda x: len(x))
        transformed_sequence = sequence
        for relation in ordered_generalized_relations:
            #relation is sth like [0,1,2,2]
            if 2 * len(sequence) >= len(relation) and position_of_list_in_list(sequence, relation) >= 0:
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
        for variable in self.retrieveVariablesFromElement(element_string):
            element_string = element_string.replace(variable, self.generators[variable])
        element_list = element_string.split(MULTIPLICATION_SIGN)
        element = []
        for term in element_list:
            #term is sth like x0^3, 1
            if term.find(NEUTRAL_ELEMENT) >= 0:
                pass
            elif EXPONENT_SIGN in term:
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
            expression += "%s%s%d%s" % (self.reversed_generators[VARIABLE + str(pair[0])], EXPONENT_SIGN, pair[1], MULTIPLICATION_SIGN)
        expression += END_OF_EQUATION
        expression = expression.replace(MULTIPLICATION_SIGN + END_OF_EQUATION, END_OF_EQUATION)
        return expression
    
    def _elementToElementString(self, element):
        element_string = ""
        pairs = []
        if len(element) > 0:
            if element[0] <= self.nb_generators:
                pairs.append([element[0], 1])
            else:
                pairs.append([self._index_of_inverse(element[0]), -1])
        for i in range(1, len(element)):
            if (element[i] == element[i-1] or element[i]==self._index_of_inverse(element[i-1])) and element[i] <= self.nb_generators:
                pairs[-1][1] += 1
            elif (element[i] == element[i-1] or element[i]==self._index_of_inverse(element[i-1])) and element[i] > self.nb_generators:
                pairs[-1][1] -= 1
            elif element[i] <= self.nb_generators:
                pairs.append([element[i], 1])
            elif element[i] > self.nb_generators:
                pairs.append([self._index_of_inverse(element[i]), -1])

        for pair in pairs:
            if pair[1] != 0:
                element_string += "%s%s%d%s" % ( self.reversed_generators[VARIABLE + str(pair[0])], EXPONENT_SIGN, pair[1], MULTIPLICATION_SIGN)
        if len(element_string) > 0 and element_string[-1] == MULTIPLICATION_SIGN:
            element_string = element_string[:-1]
        element_string = element_string.replace("%s1" % EXPONENT_SIGN, "")
        if element_string == "":
            element_string = NEUTRAL_ELEMENT
        return element_string

    def retrieveVariablesFromExpression(self, expression):
        regex = re.compile('[^a-zA-Z]')
        simplified_expression = regex.sub('', expression)
        variables = set(list(simplified_expression))
        index = len(self.generators)
        for character in sorted(list(variables)):
            if character != "e":
                if character not in self.generators.keys():
                    self.generators[character] = "x" + str(index)
                    expression = expression.replace(character, "$" + str(index))
                    index += 1
                else:
                    expression = expression.replace(character, self.generators[character].replace("x", "$"))
                    
        expression = expression.replace("$", "x")
        return expression
    
    def retrieveVariablesFromElement(self, element):
        regex = re.compile('[^a-zA-Z]')
        simplified_element = regex.sub('', element)
        variables = set(list(simplified_element))
        return sorted(list(variables))
    
    def _listElementsOfLength(self, length):
        all_classes = []
        if length==0:
            all_classes.append([])
            return all_classes
        for element in self._listElementsOfLength(length-1):
            for index in range (1, 2*self.nb_generators + 1):
                new_element = element + [index]
                if self.commutative:
                    new_element = self._sortElementInCommutativeGroup(new_element)
                    if len(new_element) == length and new_element not in all_classes:
                        all_classes.append(self._sortElementInCommutativeGroup(new_element))
                elif len(self._simplify(new_element)) == length and new_element not in all_classes:
                    all_classes.append(new_element)
        return all_classes
    
    def _listAllElements(self):
        all_classes = []
        for length in range(self.nb_terms_in_simplest_form + 1):
            all_classes += self._listElementsOfLength(length)
        
        distinct_classes = []
        for some_class in all_classes:
            is_new = True
            for another_class in distinct_classes:
                try:
                    if self._areEqual(some_class, another_class):
                        is_new = False
                        break
                except:
                    print "Unable to multiply"
                    pass
            if is_new:
                distinct_classes.append(some_class)
        
        return distinct_classes

    def _checkCommutative(self):
        if self.commutative:
            return True
        for generator in range(1, self.nb_generators + 1):
            for another_generator in range(1, self.nb_generators + 1):
                if not self._areEqual([generator, another_generator], [another_generator, generator]):
                    return False
        return True
    
    def _sortElementInCommutativeGroup(self, element):
        if not self.commutative:
            return element
        preres = [0] * (self.nb_generators + 1)
        for term in element:
            #term is sth like 1 or 2 or 3
            if term <= self.nb_generators:
                preres[term] += 1
            else:
                preres[self._index_of_inverse(term)] -= 1
        res = []
        for generator in range(1, self.nb_generators + 1):
            if preres[generator] > 0:
                res += [generator] * preres[generator]
            elif preres[generator] < 0:
                res += [self._index_of_inverse(generator)] * (-preres[generator])
        return res
    
    def _createMultiplicationTable(self):
        multi_tab = []
        for idx1 in range(self.order):
            row = []
            for idx2 in range(self.order):
                if self.commutative:
                    row += [self._simplify(self._sortElementInCommutativeGroup(self._multiply(self.all_elements[idx1], self.all_elements[idx2])))]
                else:
                    row += [self._simplify(self._multiply(self.all_elements[idx1], self.all_elements[idx2]))]
            multi_tab += [row]
        return multi_tab
    
    def createMultiplicationTable(self):
        multi_tab = self._createMultiplicationTable()
        multi_string_tab = [[self._elementToElementString(element) for element in row] for row in multi_tab]
        return multi_string_tab
        
#------------------------MAIN-------------------------

groups = {}

#GROUPS OF ORDER 2
groups["02 - Z/2Z"] = GroupByGeneratorsAndRelations('Z/2Z', 1, ["x^2=e"], nb_terms_in_simplest_form = 1)
"""
#GROUPS OF ORDER 3
groups["03 - Z/3Z"] = GroupByGeneratorsAndRelations('Z/3Z', 1, ["x^3=e"], nb_terms_in_simplest_form = 1)

#GROUPS OF ORDER 4
groups["04 - Z/4Z"] = GroupByGeneratorsAndRelations('Z/4Z', 1, ["x^4=e"], nb_terms_in_simplest_form = 2)
groups["04 - Z/2Z x Z/2Z"] = GroupByGeneratorsAndRelations('Z/2Z x Z/2Z', 2, ["x^2=e", "y^2=e", "x*y*x^-1*y^-1=e"], nb_terms_in_simplest_form = 2)

#GROUPS OF ORDER 5
groups["05 - Z/5Z"] = GroupByGeneratorsAndRelations('Z/5Z', 1, ["x^5=e"], nb_terms_in_simplest_form = 2)

#GROUPS OF ORDER 6
groups["06 - Z/6Z"] = GroupByGeneratorsAndRelations('Z/6Z', 1, ["x^6=e"], nb_terms_in_simplest_form = 3)
groups["06 - D3"] = GroupByGeneratorsAndRelations('D3', 2, ["x^2=e", "y^3=e", "x*y*x*y=e"], nb_terms_in_simplest_form = 2)

#GROUPS OF ORDER 7
groups["07 - Z/7Z"] = GroupByGeneratorsAndRelations('Z/7Z', 1, ["x^7=e"], nb_terms_in_simplest_form = 3)


#GROUPS OF ORDER 8
groups["08 - Z/8Z"] = GroupByGeneratorsAndRelations('Z/8Z', 1, ["x^8=e"], nb_terms_in_simplest_form = 4)
groups["08 - Z/2Z x Z/4Z"] = GroupByGeneratorsAndRelations('Z/4Z x Z/2Z', 2, ["x^4=e", "y^2=e", "x*y*x^-1*y^-1=e"], nb_terms_in_simplest_form = 3)
groups["08 - (Z/2Z)^3"] = GroupByGeneratorsAndRelations('(Z/2Z)^3', 3, ["x^2=e", "y^2=e", "z^2=e", "x*y*x^-1*y^-1=e", "y*z*y^-1*z^-1=e", "z*x*z^-1*x^-1=e"], nb_terms_in_simplest_form = 3)
groups["08 - Q8"] = GroupByGeneratorsAndRelations('Q8', 2, ["x^4=e", "y*y*x^-1*x^-1=e", "y*x*y^-1*x=e"], nb_terms_in_simplest_form = 2)
#groups['Q8'] = GroupByGeneratorsAndRelations('Quaternion', 2, ["y*x*y*x^-1=e", "x*y*x*y^-1=e"], nb_terms_in_simplest_form = 2)
groups["08 - D4"] = GroupByGeneratorsAndRelations('D4', 2, ["x^2=e", "y^4=e", "x*y*x*y=e"], nb_terms_in_simplest_form = 3)

#GROUPS OF ORDER 9
groups["09 - Z/9Z"] = GroupByGeneratorsAndRelations('Z/9Z', 1, ["x^9=e"], nb_terms_in_simplest_form = 4)
groups["09 - Z/3Z x Zx3Z"] = GroupByGeneratorsAndRelations('Z/3Z x Z/3Z', 2, ["x^3=e", "y^3=e", "x*y*x^-1*y^-1=e"], nb_terms_in_simplest_form = 2)

#GROUP OF ORDER 10
groups["10 - Z/10Z"] = GroupByGeneratorsAndRelations('Z/10Z', 1, ["x^10=e"], nb_terms_in_simplest_form = 5)
groups["10 - D5"] = GroupByGeneratorsAndRelations('D5', 2, ["x^2=e", "y^5=e", "x*y*x*y=e"], nb_terms_in_simplest_form = 3)

#GROUP OF ORDER 11
groups["11 - Z/11Z"] = GroupByGeneratorsAndRelations('Z/11Z', 1, ["x^11=e"], nb_terms_in_simplest_form = 5)

#GROUP OF ORDER 12
groups["12 - Z/12Z"] = GroupByGeneratorsAndRelations('Z/12Z', 1, ["x^12=e"], nb_terms_in_simplest_form = 6)
groups["12 - Z/2Z x Zx6Z"] = GroupByGeneratorsAndRelations('Z/2Z x Z/6Z', 2, ["x^2=e", "y^6=e", "x*y*x^-1*y^-1=e"], nb_terms_in_simplest_form = 4)
groups["12 - D6"] = GroupByGeneratorsAndRelations('D6', 2, ["x^2=e", "y^6=e", "x*y*x*y=e"], nb_terms_in_simplest_form = 4)
groups["12 - Dic12"] = GroupByGeneratorsAndRelations('Dic12', 2, ["y^6=e", "x^2*y^-3=e", "x^-1*y*x*y=e"], nb_terms_in_simplest_form = 4)
groups["12 - A4"] = GroupByGeneratorsAndRelations('A4', 2, ["x^2=e", "y^3=e", "x*y*x*y*x*y=e"], nb_terms_in_simplest_form = 3)

#GROUP OF ORDER 13
groups["13 - Z/13Z"] = GroupByGeneratorsAndRelations('Z/13Z', 1, ["x^13=e"], nb_terms_in_simplest_form = 6)

#GROUP OF ORDER 14
groups["14 - Z/14Z"] = GroupByGeneratorsAndRelations('Z/14Z', 1, ["x^14=e"], nb_terms_in_simplest_form = 7)
groups["14 - Z/14Z"] = GroupByGeneratorsAndRelations('D7', 2, ["x^2=e", "y^7=e", "x*y*x*y=e"], nb_terms_in_simplest_form = 7)

#GROUP OF ORDER 15
groups["15 - Z/15Z"] = GroupByGeneratorsAndRelations('Z/15Z', 1, ["x^15=e"], nb_terms_in_simplest_form = 7)


#GROUP OF ORDER 16
groups["16 - Z/16Z"] = GroupByGeneratorsAndRelations('Z/16Z', 1, ["x^16=e"], nb_terms_in_simplest_form = 8)
groups["16 - Z/4Z x Z/4Z"] = GroupByGeneratorsAndRelations('Z/4Z x Z/4Z', 2, ["x^4=e", "y^4=e", "x*y*x^-1*y^-1=e"], nb_terms_in_simplest_form = 4)
groups["16 - Z/4Z x Z/2Z x Z/2Z"] = GroupByGeneratorsAndRelations('Z/4Z x Z/2Z x Z/2Z', 3, ["x^4=e", "y^2=e", "z^2=e", "x*y*x^-1*y^-1=e", "y*z*y^-1*z^-1=e", "z*x*z^-1*x^-1=e"], nb_terms_in_simplest_form = 4)
"""
