# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 17:17:36 2017

@author: ndoannguyen
"""

import re
from Syllable import Syllable

class Word:
    def __init__(self, word):
        self.word = word
        self.splitWordToSyllables()
    
    def splitWordToSyllables(self):
        self.raw_syllables = re.split('[ |\-|_]+', self.word)
        self.syllables = [Syllable(syllable) for syllable in self.raw_syllables]
    
    def getWord(self):
        return self.word
    
    def getSyllables(self):
        return self.syllables
    
    def getRhyme(self):
        return self.syllables[-1].getRhyme()
    
    def getAccent(self):
        return self.syllables[-1].getAccent()
    
    def getLength(self):
        return len(self.syllables)

word1 = Word("nhà Trắng")
print word1.getLength()