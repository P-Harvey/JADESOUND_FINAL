# JADESOUND FP
# 20211207

import numpy as np
import pandas as pd
import scipy as sp
import scikits.bootstrap as bootstrap
import statsmodels.api as sm
import statsmodels.stats as smstats
import os
import csv

def leastSquares(X, y):
    olsFit = sm.regression.linear_model.OLS(y, X).fit()
    return olsFit

def summStat(r):
    print(r.summary())
    return

def descrStats(data):
    descr = smstats.descriptivestats.describe(data)
    return descr
    
    
def loadcsv(filename):
    """
    Load CSV file into list-of-dictionaries format
    Input: string name of file to be loaded
    Output: list of observations contained in file
    """
    data = []
    if filename in os.listdir("data/") and filename.endswith(".csv"):
        f = open("data/"+filename)
        reader = csv.reader(f)
        keys = []
        for row in reader:
            if keys == []:
                keys = row
            
            else:
                entry= {}
                for key, value in zip(keys, row):
                    entry[key] = value
                data.append(entry)
    
    if data == []: print("Error: No data acquired.")
    return data
    
        
def extract_subset(data, keys):
    """
    For pulling subsets of variable:value pairs from larger observation sets.
    Inputs:
            data: dataset in the form of a list of {variable:value} dictionaries
            keys: variables to be extracted into the subset
    Output: list of {variable:value} dictionaries containing just the variables in keys
    """
    subSet = []
    for obs in data:
        subObs = dict.fromkeys(keys)
        for key in keys:
            subObs[key] = obs[key]
        subSet.append(subObs)
    
    return subSet
    
def sort_by_key(observation, key=""):
    """
    General skeleton function for sorting list of dictionaries by a specific key.
    We can copy and modify to make it more task specific as needed.
    Call in the "key" argument of sorted() as sort_by_key(key=X)
    """
    return observation[key]

def test():
    d = [1,2,3,4,5,6,7,8,9,10]
    d1 = [10,9,8,7,6,5,4,3,2,1]
    dataframe = {'X':d,"y":d1}
    df = pd.DataFrame(dataframe)
    fit = leastSquares(d, d1)
    summStat(fit)
    descriptions = descrStats(df)
    print(descriptions)
    
#test()
