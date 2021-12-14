# JADESOUND FP
# 20211207
import numpy as np
import pandas as pd
import scipy as sp
#import scikits.bootstrap as bootstrap
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
    
def county_pop_percent(state_supplement, county_supplement):
    '''
    

    Parameters
    ----------
    state_supplement : DataFrame
        data on state's populations.
    county_supplement : DataFrame
        data on county's populations.

    Returns
    -------
    pop_percent : dict
        pyhton dictionary of dictionaries
        key is states and value is a dictionary where key is county and value is pop% for state.

    '''
    #Trim to just 2018 pop
    state_pop = state_supplement.loc[state_supplement['Variable_Code'] == 'State_Population_2018']
    county_pop = county_supplement.loc[county_supplement['Variable_Code'] == 'Population_Estimate_2018']
    
    pop_percent = {}
    state_dict = {}
    
    state = county_pop.iloc[0]['State'] # first state in data (should be AL)
    pop_state = state_pop[state_pop['State'] == state].iloc[0]['Value'] # pop for first state
    '''
    make a new dictionary for each state
    then add that dictionary to master dictionary when done w each state
    '''
    for county_index in range(len(county_pop['County'])): # iterating over every county
        if state == county_pop.iloc[county_index]['State']:
            
            # same state as previous
            county = county_pop.iloc[county_index]['County']
            pop_county = county_pop.iloc[county_index]['Value']
            state_dict[county] = pop_county/pop_state
            
        else:
            
            # next state
            pop_percent[state] = state_dict # add prevoius state to master dict
            state_dict = {} # clear previous states dictionary
            
            state = county_pop.iloc[county_index]['State']
            pop_state = state_pop[state_pop['State'] == state].iloc[0]['Value']
            county = county_pop.iloc[county_index]['County']
            pop_county = county_pop.iloc[county_index]['Value']
            state_dict[county] = pop_county/pop_state
        
    return pop_percent
                
        
    

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

    pop_percent = county_pop_percent(state_supplement, county_supplement)

    #Trim to just data by state
    indicator_seven_days = indicator_seven_days.loc[indicator_seven_days["Group"] == "By State"]
    indicator_four_weeks = indicator_four_weeks.loc[indicator_four_weeks["Group"] == "By State"]

    pop_data = county_supplement.loc[county_supplement["Variable_Code"] == "Population_Estimate_2015"]
    for county in pop_data["County"]:
        county = county[0:-7]
        
    low_access_10 = calc_percents(state_and_county, pop_data, "LACCESS_POP10")
    low_access_15 = calc_percents(state_and_county, pop_data, "LACCESS_POP15")
    lacc10_15_pearson = pearson(low_access_10["Percentage"], low_access_15["Percentage"])
    
    i7_anxiety = indicator_seven_days.loc[indicator_seven_days['Indicator'] == 'Symptoms of Anxiety Disorder']
    i4_delayed = indicator_four_weeks.loc[indicator_four_weeks['Indicator'] == 'Delayed Medical Care, Last 4 Weeks']
    
    #anxiety_delayed_care_pearson = pearson(indicator_seven_days.loc[indicator_seven_days['Indicator'] == 'Symptoms of Anxiety Disorder'],
        #                                  indicator_four_weeks.loc[indicator_four_weeks['Indicator'] == 'Delayed Medical Care, Last 4 Weeks'])
    #print(anxiety_delayed_care_pearson)