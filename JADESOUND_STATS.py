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

def pearson(X, y):
    """
    Parameters
    ----------
    X : Column of DataFrame
        Variable 1
    y : Column of DataFrame
        Variable 2

    Returns
    -------
    pearson_p : tuple
        Value one = Pearson's correlation coefficient
        Value two = two-tailed p-value
    """
    pearson_p = sp.stats.pearsonr(X, y)
    return pearson_p

def calc_percents(data, pop_data, variable):

    outdata = pd.DataFrame(columns=["State", "Percentage", "Population"])
    state_df = pop_data[["State","Value"]]
    state_df['State'].str.strip()
    state_df.set_index('State', inplace=True)
    var_df = data[["State", "Variable_Code", "Value"]]
    var_df = var_df.loc[var_df["Variable_Code"] == variable]
    for state in abr.values():
        try:
            total_pop = state_df.loc[[state]].sum()
            var_count = var_df.loc[data["State"] == state].sum()
            perc_pop = var_count.Value/total_pop.Value
        except KeyError:
            total_pop = 0
            var_count = pd.Series([0,0,0], index=['State',"Variable_Code", "Value"])
            perc_pop = 0
        new_line = {"State":state, "Percentage":perc_pop, "Population":var_count.Value}
        outdata = outdata.append(new_line, ignore_index=True)
    return outdata

def test():
    d = [1,2,3,4,5,6,7,8,9,10]
    d1 = [10,9,8,7,6,5,4,3,2,1]
    dataframe = {'X':d,"y":d1}
    df = pd.DataFrame(dataframe)
    fit = leastSquares(d, d1)
    summStat(fit)
    descriptions = descrStats(df)
    print(descriptions)

if __name__ == '__main__':
    indicator_seven_days = pd.read_csv("data/Indicators_of_Anxiety_or_Depression_Based_on_Reported_Frequency_of_Symptoms_During_Last_7_Days.csv")
    indicator_four_weeks = pd.read_csv("data/Indicators_of_Reduced_Access_to_Care_Due_to_the_Coronavirus_Pandemic_During_Last_4_Weeks.csv")
    state_and_county = pd.read_csv("data/StateAndCountyData.csv")
    state_and_county = state_and_county.astype({"FIPS":str,
                                                "State":str,
                                                "County":str,
                                                "Variable_Code":str,
                                                "Value":float})
    variable_list = pd.read_csv("data/VariableList.csv")
    county_supplement = pd.read_csv("data/SupplementalDataCounty.csv", skipinitialspace = True)

    #Trim to just data by state
    indicator_seven_days = indicator_seven_days.loc[indicator_seven_days["Group"] == "By State"]
    indicator_four_weeks = indicator_seven_days.loc[indicator_seven_days["Group"] == "By State"]

    pop_data = county_supplement.loc[county_supplement["Variable_Code"] == "Population_Estimate_2015"]
    for county in pop_data["County"]:
        county = county[0:-7]
        
    low_access_10 = calc_percents(state_and_county, pop_data, "LACCESS_POP10")
    low_access_15 = calc_percents(state_and_county, pop_data, "LACCESS_POP15")
    lacc10_15_pearson = pearson(low_access_10["Percentage"], low_access_15["Percentage"])
