# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 18:10:57 2017

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

V_PURE_CONSONANTS = ["b", "c", "ch", "d", "đ", "g", "gi", "h", "l", "m", "n", "ng", "nh", "ph", "r", "s", "t", "th", "tr", "v", "x"]

V_PURE_PRIMARY_PARTS = ["a", "ă", "â", "e", "ê", "i", "o", "ô", "ơ", "u", "ư", "iê", "uô", "ươ"]

V_PURE_SECONDARY_PARTS = ["u"]

V_PURE_END_PARTS = ["n", "t", "ng", "c", "m", "p", "nh", "ch", "i", "u"]

V_PURE_ACCENTS = ["z", "f", "s", "r", "x", "j"]
                              
UPPER_CONSONANT_VLETTER_LIST = CONSONANT_VLETTER_DICTIONARY.keys()
UPPER_VOWEL_VLETTER_LIST = VOWEL_VLETTER_DICTIONARY.keys()
UPPER_VLETTER_LIST = UPPER_CONSONANT_VLETTER_LIST + UPPER_VOWEL_VLETTER_LIST

LOWER_CONSONANT_VLETTER_LIST = CONSONANT_VLETTER_DICTIONARY.values()
LOWER_VOWEL_VLETTER_LIST = VOWEL_VLETTER_DICTIONARY.values()
LOWER_VLETTER_LIST = LOWER_CONSONANT_VLETTER_LIST + LOWER_VOWEL_VLETTER_LIST

VLETTER_LIST = UPPER_VLETTER_LIST + LOWER_VLETTER_LIST

BASIC_DATA_DIR = "D:/Userfiles/ndoannguyen/Documents/Python Scripts/VietnameseLanguage/BasicData/"
RAW_WORDS_FILE_NAME = "AllRawWords.txt"
PURE_VNESE_WORDS_FILE_NAME = "AllPureVietnameseWords.txt"
PURE_VNESE_SYLLABLES_FILE_NAME = "AllPureVietnameseSyllables.txt"
RHYMES_FILE_NAME = "AllRhymes.txt"
FREQUENCY_OF_WORD_FILE_NAME = "Statistics_12-1707.txt"