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
                keys = [key.strip() for key in row]
            
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
    
def extract_by_value(data, key, value):
    """
    For extracting every observation whose specified key has the specified value
    """
    subSet = []
    for obs in data:
        if obs[key] == value:
            subSet.append(obs)
    
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
    
def main():
    indicator_seven_days = loadcsv("Indicators_of_Anxiety_or_Depression_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv")
    indicator_four_weeks = loadcsv("Indicators_of_Reduced_Access_to_Care_Due_to_the_Coronavirus_Pandemic_During_Last_4_Weeks.csv")
    state_and_county = loadcsv ("StateAndCountyData.csv")
    variable_list = loadcsv("VariableList.csv")
    
    #get code meanings, swap them in for the state and county observations
    code_meanings = {}
    variable_correspondences = extract_subset(variable_list, ["\ufeffVariable_Name", "Variable_Code"])
    for code in variable_correspondences:
        variable_code = code["Variable_Code"]
        variable_name = code["\ufeffVariable_Name"]
        code_meanings[variable_code] = variable_name
    
    #Trim to just data by state
    indicator_seven_days = extract_by_value(indicator_seven_days, "Group", "By State")
    indicator_four_weeks = extract_by_value(indicator_four_weeks, "Group", "By State")
    
    #populations of counties in 2015
    county_populations = extract_by_value(state_and_county, 
    
main()
