# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:38:57 2017

@author: ndoannguyen
"""

import Constants

class Rhyme:
    def __init__(self, secondary_part, primary_part, end_part):
        self.secondary_part = secondary_part
        self.primary_part = primary_part
        self.end_part = end_part
    
    def getSecondaryPart(self):
        return self.secondary_part
    
    def setSecondaryPart(self, secondary_part):
        self.secondary_part = secondary_part
    
    def getPrimaryPart(self):
        return self.primary_part
    
    def setPrimaryPart(self, primary_part):
        self.primary_part = primary_part
    
    def getEndPart(self):
        return self.end_part
        
    def setEndPart(self, end_part):
        self.end_part = end_part
        
    def isQuasiRhymable(self, AnotherRhyme):
        """
            Kiểm tra 2 vần có được xem là gần vần với nhau hay không.
            Dưới đây liệt kê các trường hợp được coi là gần vần
            Đây là hàm phụ, sẽ được sử dụng cho areRhymable(syllable1, syllable2)
        """
        b1, c1 = self.primary_part, self.end_part
        b2, c2 = AnotherRhyme.primary_part, AnotherRhyme.end_part
        if c1 in ['n', 'ng'] and c2 in ['n', 'ng'] and b1 in ['a', 'ă', 'â', 'e', 'iê', 'uô', 'ươ'] and b2 == b1:
            return True
        elif c1 in ['t', 'c'] and c2 in ['t', 'c'] and b1 in ['a', 'ă', 'â', 'e', 'ư', 'iê', 'uô', 'ươ'] and b2 == b1:
            return True
        elif c1 in ['n', 'nh'] and c2 in ['n', 'nh'] and b1 in ['ê', 'i'] and b2 == b1:
            return True
        elif c1 in ['t', 'ch'] and c2 in ['t', 'ch'] and b1 in ['ê', 'i'] and b2 == b1:
            return True
        elif c1 == 'u' and c2 == 'u':
            if b1 in ['a', 'ă', 'â'] and b2 in ['a', 'ă', 'â']:
                return True
            elif b1 in ['e', 'ê'] and b2 in ['e', 'ê']:
                return True
            elif b1 in ['ê', 'i', 'iê'] and b2 in ['ê', 'i', 'iê']:
                return True
            elif b1 in ['ư', 'ươ'] and b2 in ['ư', 'ươ']:
                return True
        elif c1 == 'i' and c2 == 'i':
            if b1 in ['a', 'ă', 'â'] and b2 in ['a', 'ă', 'â']:
                return True
            elif b1 in ['o', 'ô', 'ơ'] and b2 in ['o', 'ô', 'ơ']:
                return True
            elif b1 in ['u', 'uô'] and b2 in ['u', 'uô']:
                return True
            elif b1 in ['ơ', 'ư', 'ươ'] and b2 in ['ơ', 'ư', 'ươ']:
                return True
        return False
