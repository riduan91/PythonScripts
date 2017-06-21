# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 18:08:18 2017

@author: ndoannguyen
"""

CONSONANT_VLETTER_DICTIONARY = {"B":"b", "C":"c", "D":"d", "Đ":"đ", "E":"e", "F":"f", "G":"g", 
                               "H":"h", "J":"j", "K":"k", "L":"l", "M":"m", "N":"n", "P":"p",
                               "Q":"q", "R":"r", "S":"s", "T":"t", "V":"v", "W":"w", "X":"x",
                               "Z":"z"
                               }
                               
VOWEL_VLETTER_DICTIONARY = {"A":"a", "Ă":"ă", "Â":"â", "E":"e", "Ê":"ê", "I":"i", "O":"o", "Ô":"ô", "Ơ":"ơ", "U":"u", "Ư":"ư", "Y":"y",
                           "À":"à", "Ằ":"ằ", "Ầ":"ầ", "È":"è", "Ề":"ề", "Ì":"ì", "Ò":"ò", "Ồ":"ồ", "Ờ":"ờ", "Ù":"ù", "Ừ":"ừ", "Ỳ":"ỳ",
                           "Á":"á", "Ắ":"ắ", "Ấ":"ấ", "É":"é", "Ế":"ế", "Í":"í", "Ó":"ó", "Ố":"ố", "Ớ":"ớ", "Ú":"ú", "Ứ":"ứ", "Ý":"ý",
                           "Ả":"ả", "Ẳ":"ẳ", "Ẩ":"ẩ", "Ẻ":"ẻ", "Ể":"ể", "Ỉ":"ỉ", "Ỏ":"ỏ", "Ổ":"ổ", "Ở":"ở", "Ủ":"ủ", "Ử":"ử", "Ỷ":"ỷ",
                           "Ã":"ã", "Ẵ":"ẵ", "Ẫ":"ẫ", "Ẽ":"ẽ", "Ễ":"ễ", "Ĩ":"ĩ", "Õ":"õ", "Ỗ":"ỗ", "Ỡ":"ỡ", "Ũ":"ũ", "Ữ":"ữ", "Ỹ":"ỹ",
                           "Ạ":"ạ", "Ặ":"ặ", "Ậ":"ậ", "Ẹ":"ẹ", "Ệ":"ệ", "Ị":"ị", "Ọ":"ọ", "Ộ":"ộ", "Ợ":"ợ", "Ụ":"ụ", "Ự":"ự", "Ỵ":"ỵ",
                           }
                           
REMOVE_ACCENT_FROM_VLETTER = {
                              "à":"a", "ằ":"ă", "ầ":"â", "è":"e", "ề":"ê", "ì":"i", "ò":"o", "ồ":"ô", "ờ":"ơ", "ù":"u", "ừ":"ư", "ỳ":"y",
                              "á":"a", "ắ":"ă", "ấ":"â", "é":"e", "ế":"ê", "í":"i", "ó":"o", "ố":"ô", "ớ":"ơ", "ú":"u", "ứ":"ư", "ý":"y",
                              "ả":"a", "ẳ":"ă", "ẩ":"â", "ẻ":"e", "ể":"ê", "ỉ":"i", "ỏ":"o", "ổ":"ô", "ở":"ơ", "ủ":"u", "ử":"ư", "ỷ":"y",
                              "ã":"a", "ẵ":"ă", "ẫ":"â", "ẽ":"e", "ễ":"ê", "ĩ":"i", "õ":"o", "ỗ":"ô", "ỡ":"ơ", "ũ":"u", "ữ":"ư", "ỹ":"y",
                              "ạ":"a", "ặ":"ă", "ậ":"â", "ẹ":"e", "ệ":"ê", "ị":"i", "ọ":"o", "ộ":"ô", "ợ":"ơ", "ụ":"u", "ự":"ư", "ỵ":"y",
                              }

TAKE_ACCENT_FROM_VLETTER = {
                              "à":"f", "ằ":"f", "ầ":"f", "è":"f", "ề":"f", "ì":"f", "ò":"f", "ồ":"f", "ờ":"f", "ù":"f", "ừ":"f", "ỳ":"f",
                              "á":"s", "ắ":"s", "ấ":"s", "é":"s", "ế":"s", "í":"s", "ó":"s", "ố":"s", "ớ":"s", "ú":"s", "ứ":"s", "ý":"s",
                              "ả":"r", "ẳ":"r", "ẩ":"r", "ẻ":"r", "ể":"r", "ỉ":"r", "ỏ":"r", "ổ":"r", "ở":"r", "ủ":"r", "ử":"r", "ỷ":"r",
                              "ã":"x", "ẵ":"x", "ẫ":"x", "ẽ":"x", "ễ":"x", "ĩ":"x", "õ":"x", "ỗ":"x", "ỡ":"x", "ũ":"x", "ữ":"x", "ỹ":"x",
                              "ạ":"j", "ặ":"j", "ậ":"j", "ẹ":"j", "ệ":"j", "ị":"j", "ọ":"j", "ộ":"j", "ợ":"j", "ụ":"j", "ự":"j", "ỵ":"j",
                              }

GI_INCOMPATIBLE = ["a", "ă", "â", "e", "o", "ô", "ơ", "u", "ư"]

GI_COMPATIBLE = ["i", "ê"]
                              
UPPER_CONSONANT_VLETTER_LIST = CONSONANT_VLETTER_DICTIONARY.keys()
UPPER_VOWEL_VLETTER_LIST = VOWEL_VLETTER_DICTIONARY.keys()
UPPER_VLETTER_LIST = UPPER_CONSONANT_VLETTER_LIST + UPPER_VOWEL_VLETTER_LIST

LOWER_CONSONANT_VLETTER_LIST = CONSONANT_VLETTER_DICTIONARY.values()
LOWER_VOWEL_VLETTER_LIST = VOWEL_VLETTER_DICTIONARY.values()
LOWER_VLETTER_LIST = LOWER_CONSONANT_VLETTER_LIST + LOWER_VOWEL_VLETTER_LIST

VLETTER_LIST = UPPER_VLETTER_LIST + LOWER_VLETTER_LIST

def areCompatibleAccents(accent1, accent2):
    """
        Kiểm tra hai thanh điệu cùng bằng hoặc cùng trắc, trả lại True nếu cùng loại và False nếu khác loại hoặc vô định
    """
    type1 = 0
    type2 = 0
    if accent1 in "zf":
        type1 = 1
    elif accent1 in "srxj":
        type1 = 2
    if accent2 in "zf":
        type2 = 1
    elif accent2 in "srxj":
        type2 = 2
    return (type1 != 0 and type2 != 0 and type1 == type2)

def areQuasiRhymable(rhyme1, rhyme2):
    """
        Kiểm tra 2 vần có được xem là gần vần với nhau hay không.
        Dưới đây liệt kê các trường hợp được coi là gần vần
        Đây là hàm phụ, sẽ được sử dụng cho areRhymable(syllable1, syllable2)
    """
    b1, c1 = rhyme1[1], rhyme1[2]
    b2, c2 = rhyme2[1], rhyme2[2]
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

def areRhymable(syllable1, syllable2):
    """
        Kiểm tra hai tiếng vần tuyệt đối với nhau, trả lại 
        0 nếu không hề vần
        1 nếu vần tuyệt đối
        2 nếu vần chỉ sai khác âm đệm
        3 nếu vần theo phương ngữ Nam
    """
    analysis1 = SplitSyllableToParts(syllable1)
    rhyme1, accent1 = analysis1[1], analysis1[2]
    analysis2 = SplitSyllableToParts(syllable2)
    rhyme2, accent2 = analysis2[1], analysis2[2]
    if rhyme1 == rhyme2 and areCompatibleAccents(accent1, accent2):
        return 1
    elif rhyme1[1] == rhyme2[1] and rhyme1[2] == rhyme2[2] and areCompatibleAccents(accent1, accent2):
        return 2
    elif areQuasiRhymable(rhyme1, rhyme2) and areCompatibleAccents(accent1, accent2):
        return 3
    return 0
    
def ToLowerVLetter(vletter):
    """
        Chuyển chữ cái thành in thường
    """
    if vletter in CONSONANT_VLETTER_DICTIONARY:
        return CONSONANT_VLETTER_DICTIONARY[vletter]
    elif vletter in VOWEL_VLETTER_DICTIONARY:
        return VOWEL_VLETTER_DICTIONARY[vletter]
    else:
        return vletter

def SplitSyllableToVLetters(syllable):
    """
        Tách một tiếng thành các chữ cái (chữ cái = chữ cái đội dấu thanh), giữ nguyên trạng thái viết hoa
        Ví dụ: "Tiễn -> [T, i, ễ, n]"
    """
    syllable_length = len(syllable)
    current_position = 0
    composed_vletters = []
    while (current_position != syllable_length):
        for i in range (min(3, syllable_length - current_position), 0, -1):
            if (syllable[current_position : current_position + i] in VLETTER_LIST):
                composed_vletters.append(ToLowerVLetter(syllable[current_position : current_position + i]))
                current_position += i
                break
            if i==1:
                composed_vletters.append(ToLowerVLetter(syllable[current_position]))
                current_position += 1
    return composed_vletters

def SplitSyllableToParts(syllable):
    """
        Tách một tiếng thành 3 phần: phụ âm đầu, vần và thanh
        Kí hiệu thanh: Ngang: z, Huyền: f, Sắc: s , Hỏi: r, Ngã: x, Nặng: j
    """
    composed_vletters = SplitSyllableToVLetters(syllable)
    nb_vletters = len(composed_vletters)
    beginning_consonant = ""
    rhyme = ""
    accent = "z"
    consonant_terminated = 0
    for i in range(nb_vletters):
        if composed_vletters[i] in LOWER_CONSONANT_VLETTER_LIST and consonant_terminated == 0:
            beginning_consonant += composed_vletters[i]
        elif composed_vletters[i] in REMOVE_ACCENT_FROM_VLETTER:
            rhyme += REMOVE_ACCENT_FROM_VLETTER[composed_vletters[i]]
            accent = TAKE_ACCENT_FROM_VLETTER[composed_vletters[i]]
            consonant_terminated = 1
        else:
            rhyme += composed_vletters[i]
            consonant_terminated = 1
    
    if beginning_consonant == "g" and rhyme.startswith("i"):
        beginning_consonant = "gi"
        for i in range(min(2, len(rhyme) - 1), 0, -1):
            if (rhyme[1 : 1 + i] in GI_INCOMPATIBLE):
                rhyme = rhyme[1:]
                break
    
    beginning_consonant = beginning_consonant.replace("k", "c").replace("q", "c").replace("gh", "g").replace("ngh", "ng")
    analyzed_rhyme = SplitRhymeToSmallParts(rhyme)
    return beginning_consonant, analyzed_rhyme, accent

def SplitRhymeToSmallParts(rhyme):
    """
        Tách vần thành âm đệm (secondary_part), âm chính (primary_part), âm cuối (end_part)
    """
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
    return secondary_part, primary_part, end_part

print areRhymable("ba", "a")