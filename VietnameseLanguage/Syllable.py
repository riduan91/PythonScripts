# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:08:18 2017
@author: ndoannguyen
"""

import Constants
from VLetter import ToLowerVLetter
from Accent import areCompatibleAccents

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

class Syllable:
    
    def __init__(self, syllable):
        self.syllable = syllable
        self.SplitSyllableToParts()
    
    def SplitSyllableToParts(self):
        """
        Tách một tiếng thành 3 phần: phụ âm đầu, vần và thanh
        Kí hiệu thanh: Ngang: z, Huyền: f, Sắc: s , Hỏi: r, Ngã: x, Nặng: j
        """
        self.SplitSyllableToVLetters()
        composed_vletters = self.composed_vletters
        nb_vletters = len(composed_vletters)
        beginning_consonant = ""
        rhyme = ""
        accent = "z"
        consonant_terminated = 0
        for i in range(nb_vletters):
            if composed_vletters[i] in Constants.LOWER_CONSONANT_VLETTER_LIST and consonant_terminated == 0:
                beginning_consonant += composed_vletters[i]
            elif composed_vletters[i] in Constants.REMOVE_ACCENT_FROM_VLETTER:
                rhyme += Constants.REMOVE_ACCENT_FROM_VLETTER[composed_vletters[i]]
                accent = Constants.TAKE_ACCENT_FROM_VLETTER[composed_vletters[i]]
                consonant_terminated = 1
            else:
                rhyme += composed_vletters[i]
                consonant_terminated = 1
    
        if beginning_consonant == "g" and rhyme.startswith("i"):
            beginning_consonant = "gi"
            for i in range(min(2, len(rhyme) - 1), 0, -1):
                if (rhyme[1 : 1 + i] in Constants.GI_INCOMPATIBLE):
                    rhyme = rhyme[1:]
                    break
    
        beginning_consonant = beginning_consonant.replace("k", "c").replace("q", "c").replace("gh", "g").replace("ngh", "ng")
        self.beginning_consonant = beginning_consonant
        self.raw_rhyme = rhyme
        self.accent = accent
        self.SplitRhymeToSmallParts()
    
    def SplitSyllableToVLetters(self):
        """
            Tách một tiếng thành các chữ cái (chữ cái = chữ cái đội dấu thanh), giữ nguyên trạng thái viết hoa
            Ví dụ: "Tiễn -> [T, i, ễ, n]"
        """
        syllable = self.syllable
        syllable_length = len(syllable)
        current_position = 0
        composed_vletters = []
        while (current_position != syllable_length):
            for i in range (min(3, syllable_length - current_position), 0, -1):
                if (syllable[current_position : current_position + i] in Constants.VLETTER_LIST):
                    composed_vletters.append(ToLowerVLetter(syllable[current_position : current_position + i]))
                    current_position += i
                    break
                if i==1:
                    composed_vletters.append(ToLowerVLetter(syllable[current_position]))
                    current_position += 1
        self.composed_vletters = composed_vletters 
        
    def SplitRhymeToSmallParts(self):
        """
        Tách vần thành âm đệm (secondary_part), âm chính (primary_part), âm cuối (end_part)
        """
        rhyme = self.raw_rhyme
        secondary_part = ""
        primary_part = ""
        end_part = ""
        if rhyme.startswith("oa") or rhyme.startswith("oe") or rhyme.startswith("ua") or rhyme.startswith("ue") \
            or rhyme.startswith("oă") or rhyme.startswith("uă") or rhyme.startswith("uâ")\
            or rhyme.startswith("uê") or rhyme.startswith("uy") or rhyme.startswith("uơ"):
                rhyme = rhyme[1:]
                secondary_part = "u"
        if rhyme.endswith("n") or rhyme.endswith("t") or rhyme.endswith("m") or rhyme.endswith("p") or rhyme.endswith("c"):
            end_part = rhyme[-1]
            primary_part = rhyme[:-1]
        elif rhyme.endswith("ng") or rhyme.endswith("nh") or rhyme.endswith("ch"):
            end_part = rhyme[-2:]
            primary_part = rhyme[:-2]
        elif (rhyme.endswith("o") and rhyme != "o") or (rhyme.endswith("u") and rhyme != "u"):
            end_part = "u"
            primary_part = rhyme[:-1]
            if (rhyme == "au"):
                primary_part = "ă"
        elif (rhyme.endswith("i") and rhyme != "i") or (rhyme.endswith("y") and rhyme != "y"):
            end_part = "i"
            primary_part = rhyme[:-1]
            if (rhyme == "ay"):
                primary_part = "ă"
        else:
            primary_part = rhyme
    
        primary_part = primary_part.replace("y", "i").replace("ia", "iê").replace("ua", "uô").replace("ưa", "ươ")
        self.rhyme = Rhyme(secondary_part, primary_part, end_part)
    
    def getSyllable(self):
        return self.syllable
    
    def setSyllable(self, syllable):
        self.syllable = syllable
        self.SplitSyllableToParts()
        
    def getComposedVLetters(self):
        return self.composed_vletters
        
    def getBeginningConsonant(self):
        return self.beginning_consonant
    
    def getRhyme(self):
        return self.rhyme
    
    def getAccent(self):
        return self.accent
    
    def getLength(self):
        return len(self.composed_vletters)
    
    def getTechnicalLength(self):
        return len(self.syllable)
    
    def isRhymable(self, AnotherSyllable):
        """
            Kiểm tra hai tiếng vần tuyệt đối với nhau, trả lại 
            0 nếu không hề vần
            1 nếu vần tuyệt đối
            2 nếu vần chỉ sai khác âm đệm
            3 nếu vần theo phương ngữ Nam
        """
        rhyme1, accent1 = self.getRhyme(), self.getAccent()
        rhyme2, accent2 = AnotherSyllable.getRhyme(), AnotherSyllable.getAccent()
        if rhyme1.getSecondaryPart() == rhyme2.getSecondaryPart() and rhyme1.getPrimaryPart() == rhyme2.getPrimaryPart() \
            and rhyme1.getEndPart() == rhyme2.getEndPart() and areCompatibleAccents(accent1, accent2):
            return 1
        elif rhyme1.getPrimaryPart() == rhyme2.getPrimaryPart() and rhyme1.getEndPart() == rhyme2.getEndPart() and areCompatibleAccents(accent1, accent2):
            return 2
        elif rhyme1.isQuasiRhymable(rhyme2) and areCompatibleAccents(accent1, accent2):
            return 3
        return 0
        



syllable1 = Syllable("Tiễn")
syllable2 = Syllable("yến")
print syllable1.isRhymable(syllable2)
        

