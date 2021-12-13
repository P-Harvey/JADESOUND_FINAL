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
from state_abr import abr

def leastSquares(X, y):
    olsFit = sm.regression.linear_model.OLS(y, X).fit()
    return olsFit

def summStat(r):
    print(r.summary())
    return

def descrStats(data):
    descr = smstats.descriptivestats.describe(data)
    return descr
        
def calc_percents(data, pop_data, variable):
    
    outdata = pd.Dataframe(columns=["State":abr.values(), "Percentage", "Population"])
    for state in abr.values():
        total_pop = pop_data.loc[pop_data["State"] == state].sum()
        
        

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
    indicator_seven_days = pd.read_csv("data/Indicators_of_Anxiety_or_Depression_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv")
    indicator_four_weeks = pd.read_csv("data/Indicators_of_Reduced_Access_to_Care_Due_to_the_Coronavirus_Pandemic_During_Last_4_Weeks.csv")
    state_and_county = pd.read_csv("data/StateAndCountyData.csv")
    variable_list = pd.read_csv("data/VariableList.csv")
    county_supplement = pd.read_csv("data/SupplementalDataCounty.csv")
    
    #Trim to just data by state
    indicator_seven_days = indicator_seven_days.loc[indicator_seven_days["Group"] == "By State"]
    indicator_four_weeks = indicator_seven_days.loc[indicator_seven_days["Group"] == "By State"]
    
    pop_data = county_supplement.loc[county_supplement["Variable_Code"] == "Population_Estimate_2015"]
    for county in pop_data["County"]:
        county = county[0:-7]


main()
