# -*- coding: utf-8 -*-
"""
Created on Mon Jul 03 12:17:21 2017

@author: ndoannguyen
"""
import itertools

def list_to_string(mylist):
    mylist = [str(item) for item in mylist]
    return "+".join(mylist)
    
def position_of_list_in_list(list1, list2):
    """
        list1 = [1, 2, 3]
        list2 = [0, 1, 2, 3, 4]
        return 1
        if list1 not in list2 return -1
    """
    str1, str2 = list_to_string(list1), list_to_string(list2)
    position = str2.find(str1)
    if position == -1:
        return -1
    return len(str2[:position].split("+")) - 1

def all_discrete_positions_of_list_in_list(list1, list2):
    str1, str2 = list_to_string(list1), list_to_string(list2)
    positions = []
    position = str2.find(str1)
    current_beginning = 0
    current_index = 0
    while position >= 0:
        current_index += len(str2[:position].split("+")) - 1
        positions.append(current_index)
        current_beginning = position + len(str1) + 1
        current_index += len(list1)
        str2 = str2[current_beginning:]
        position = str2.find(str1)
    return positions     
    
def remaining_of_list_after_removing(list1, list2, position):
    end_position = position + len(list1)
    return list2[:position], list2[end_position:]

def sublists(mylist):
    res = []
    for i in range(len(mylist), -1, -1):
        for j in range (0, len(mylist) - i):
            res.append(mylist[j : j + i + 1])
    return res

def all_subsets(S):
    subsets = []
    for l in range(len(S) + 1):
        subsets += list(itertools.combinations(S, l))
    return subsets