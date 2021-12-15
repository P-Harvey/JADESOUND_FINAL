# JADESOUND FP
# 20211207
import numpy as np
import pandas as pd
import scipy as sp
import scikits.bootstrap as bootstrap
#if things start breaking with no warning comment out these two lines
import warnings
warnings.filterwarnings('ignore')

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

def calc_county_percents(data, pop_data, variable):

    outdata = pd.DataFrame(columns=["State", "Percentage", "Confidence Interval", "Population"])
    state_df = pop_data[["State","County","Value"]]
    state_df['State'].str.strip()
    var_df = data.loc[data["Variable_Code"] == variable][["State", "County", "Variable_Code", "Value"]]
    for state in abr.values():
        try:
            var_counts = var_df.loc[var_df["State"] == state]
            pop_counts = state_df.loc[state_df["State"] == state][["County", "Value"]]
            merged = pd.merge(var_counts, pop_counts, on="County")
            merged["Normalized"] = merged["Value_x"] * merged["Value_y"]
            normalized_total = merged["Normalized"].sum()
            total_pop = pop_counts["Value"].sum()
            perc_pop = normalized_total/total_pop
            ci = bootstrap.ci(var_counts["Value"])
            
        except KeyError:
            total_pop = 0
            ci = [0, 0]
            perc_pop = 0
        new_line = {"State":state, "Percentage":perc_pop, "Confidence Interval":ci, "Population":total_pop}
        outdata = outdata.append(new_line, ignore_index=True)
    return outdata

def process_indicator_data(data):
    
    outdata = pd.DataFrame(columns=["State", "Percentage", "Confidence Interval"])
    for state in abr.keys():
        state_abr = abr[state]
        try:
            state_data = data.loc[data["State"] == state]
            percent = state_data["Value"].sum()/len(state_data["Value"])
            ci = bootstrap.ci(state_data["Value"])
            
        except:
            percent = 0
            ci = [0,0]
        new_line = {"State":state_abr, "Percentage":percent, "Confidence Interval":ci}
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
    state_supplement = pd.read_csv("data/SupplementalDataState.csv", skipinitialspace = True)

    #Trim to just data by state
    indicator_seven_days = indicator_seven_days.loc[indicator_seven_days["Group"] == "By State"]
    indicator_four_weeks = indicator_four_weeks.loc[indicator_four_weeks["Group"] == "By State"]

    pop_data = county_supplement.loc[county_supplement["Variable_Code"] == "Population_Estimate_2015"]
    
    for i, county in pop_data["County"].iteritems():
        if county.endswith(" County"):
            pop_data.at[i, "County"] = county[:-7]
            
        elif county.endswith(" City and Borough"):
            pop_data.at[i, "County"] = county[:-17]
            
        elif county.lower().endswith(" city"):
            pop_data.at[i, "County"] = county[:-5]
            
        elif county.endswith(" Borough"):
            pop_data.at[i, "County"] = county[:-8]
            
        elif county.endswith(" Census Area"):
            pop_data.at[i, "County"] = county[:-12]
            
        elif county.endswith(" Municipality"):
            pop_data.at[i, "County"] = county[:-13]
            
        elif county.endswith(" Parish"):
            pop_data.at[i, "County"] = county[:-7]
            
    i7_anxiety = indicator_seven_days.loc[indicator_seven_days['Indicator'] == 'Symptoms of Anxiety Disorder'][['State', 'Value', 'Confidence Interval']]
    i7_depression = indicator_seven_days.loc[indicator_seven_days['Indicator'] == 'Symptoms of Depressive Disorder'][['State', 'Value', 'Confidence Interval']]
    
    i4_delayed = indicator_four_weeks.loc[indicator_four_weeks['Indicator'] == 'Delayed Medical Care, Last 4 Weeks'][['State', 'Value', 'Confidence Interval']]
    i4_denied = indicator_four_weeks.loc[indicator_four_weeks['Indicator'] == 'Did Not Get Needed Care, Last 4 Weeks'][['State', 'Value', 'Confidence Interval']]
        
#    low_access_10 = calc_percents(state_and_county, pop_data, "LACCESS_POP10")
#    low_access_15 = calc_percents(state_and_county, pop_data, "LACCESS_POP15")
#    lacc10_15_pearson = pearson(low_access_10["Percentage"], low_access_15["Percentage"])

    if not "poverty_15.p" in os.listdir("stats/"):
        poverty_15_processed = calc_county_percents(state_and_county, pop_data, "POVRATE15")
        f = open("stats/poverty_15.p", 'wb')
        pickle.dump(poverty_15_processed, f)
        f.close()
    else:
        f = open("stats/poverty_15.p", 'rb')
        poverty_15_processed = pickle.load(f)
        f.close()
    
    if not "i7_anxiety.p" in os.listdir("stats/"):
        i7_anxiety_processed = process_indicator_data(i7_anxiety)
        f = open("stats/i7_anxiety.p", 'wb')
        pickle.dump(i7_anxiety_processed, f)
        f.close()
    else:
        f = open("stats/i7_anxiety.p", 'rb')
        i7_anxiety_processed = pickle.load(f)
        f.close()
        
    if not "i7_depression.p" in os.listdir("stats/"):
        i7_depression_processed = process_indicator_data(i7_depression)
        f = open("stats/i7_depression.p", 'wb')
        pickle.dump(i7_depression_processed, f)
        f.close()
    else:
        f = open("stats/i7_depression.p", 'rb')
        i7_depression_processed = pickle.load(f)
        f.close()
    
    if not "i4_delayed.p" in os.listdir("stats/"):
        i4_delayed_processed = process_indicator_data(i4_delayed)
        f = open("stats/i4_delayed.p", 'wb')
        pickle.dump(i4_delayed_processed, f)
        f.close()
    else:
        f = open("stats/i4_delayed.p", 'rb')
        i4_delayed_processed = pickle.load(f)
        f.close()
    
    if not "i4_denied.p" in os.listdir("stats/"):
        i4_denied_processed = process_indicator_data(i4_denied)
        f = open("stats/i4_denied.p", 'wb')
        pickle.dump(i4_denied_processed, f)
        f.close()
    else:
        f = open("stats/i4_denied.p", 'rb')
        i4_denied_processed = pickle.load(f)
        f.close()
    
    #anxiety_delayed_care_pearson = pearson(indicator_seven_days.loc[indicator_seven_days['Indicator'] == 'Symptoms of Anxiety Disorder'],
        #                                  indicator_four_weeks.loc[indicator_four_weeks['Indicator'] == 'Delayed Medical Care, Last 4 Weeks'])
    #print(anxiety_delayed_care_pearson)
