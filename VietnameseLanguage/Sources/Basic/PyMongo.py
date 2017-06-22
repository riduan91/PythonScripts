# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 10:49:44 2017

@author: ndoannguyen
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('localhost', 27017)

db = client['poems']
collection = db['poems']

# Find a document
print collection.find_one()

# Inserting a document
#new_data = {'name': 'Viet Bac', 'author': 'To Huu', 'period': 'Hien dai', 'century': 'XX', '_id': '0001'}
#new_data_id =  collection.insert_one(new_data).inserted_id
#inserted_id is a field of collection.insert_one(new_data), which is in turn an InsertOneResult instance

# insert_many(an array of documents), return inserted_ids

print collection.find_one({"_id": ObjectId('5943de0d823e3158e6884d90')})
MyCursor = collection.find({"century":{"$lte": "XX"}})
print MyCursor.count()