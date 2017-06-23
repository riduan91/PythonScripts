# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 10:59:17 2017

@author: ndoannguyen
"""

BASIC_SOURCE_DIR = "D:/Userfiles/ndoannguyen/Documents/Python Scripts/VietnameseLanguage/Sources/Basic/"

import sys
sys.path.append(BASIC_SOURCE_DIR)
from Rhyme import Rhyme
import Constants

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

mongo_client = MongoClient('localhost', 27017)

VietnameseDB = mongo_client['Vietnamese']
RhymeCollection = VietnameseDB['Rhymes']

BASIC_DATA_DIR = Constants.BASIC_DATA_DIR
RHYMES_FILE_NAME = Constants.RHYMES_FILE_NAME

all_rhymes = []

reader = open(BASIC_DATA_DIR + RHYMES_FILE_NAME)
for line in reader:
    line = line.replace("\n", "").split("-")
    rhyme = Rhyme(line[0], line[1], line[2])
    all_rhymes.append(rhyme)

index = 1

for rhyme in all_rhymes:
    quasi_rhymable_rhymes = []
    for another_rhyme in all_rhymes:
        if rhyme.isQuasiRhymable(another_rhyme):
            quasi_rhymable_rhymes.append(another_rhyme.getRhyme())
    rhyme_mongo_document = {
                        "_id": "RHY" + str(index).zfill(5),
                        "rhyme" : rhyme.getRhyme(),
                        "secondary_part" : rhyme.getSecondaryPart(),
                        "primary_part" : rhyme.getPrimaryPart(),
                        "end_part" : rhyme.getEndPart(),
                        "quasi_rhymable_rhymes" : quasi_rhymable_rhymes
                    }
    try:
        RhymeCollection.insert_one(rhyme_mongo_document)
        index += 1
    except DuplicateKeyError:
        print "[Error] Rhyme with id %s already exists." % ("RHY" + str(index).zfill(5))
        index += 1