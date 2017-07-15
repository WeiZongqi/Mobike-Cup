#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 22:19:13 2017

@author: yujia
"""
import numpy as np
import pandas as pd

split_ratio = 0.8

print('************** M O B I K E  C U P  T E A M XXXXXXXXXXX ***************\n')
print('Importing data...\n')
# PATH NEED TO BE MODIFIED
dataset = pd.read_csv('data/train.csv', header=0, sep=',')
N = len(dataset)

user = dataset.userid.unique()

loc_start = dataset.geohashed_start_loc.unique()
loc_end = dataset.geohashed_end_loc.unique()

loc = np.unique(np.concatenate((loc_start, loc_end),axis = 0))

#This split might need modification. Not random enough (or I do not know if should random)
print('Splitting data...\n')
data_train = dataset[:int(N*split_ratio)]
data_test = dataset[int(N*split_ratio):]

print('Training...\n')
user_loc = {i:[] for i in user}

#This step is a bit slow. Might not be a good way to iterate            
for i in range(int(N*split_ratio)):
    user_loc[data_train.ix[i]['userid']].append(data_train.ix[i]['geohashed_end_loc'])

predict = {}
for i in user:
    if len(user_loc[i])!=0:
        predict[i] = max(set(user_loc[i]), key=user_loc[i].count)  
    else:
        predict[i] = None

print('Testing...\n')
result = []
for i in range(int(N*split_ratio),N):
    if data_test.ix[i]['geohashed_end_loc']==predict[data_test.ix[i]['userid']]:
        result.append(True)
    elif data_test.ix[i]['geohashed_end_loc']==None:
        pass
    else:
        result.append(False)
        
final_result = np.mean(result)