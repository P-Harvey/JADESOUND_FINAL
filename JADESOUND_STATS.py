# JADESOUND FP
# 20211207

import numpy as np
import pandas as pd
import scipy as sp
import statsmodels.api as sm
import statsmodels.stats as smstats

def leastSquares(X, y):
    olsFit = sm.regression.linear_model.OLS(y, X).fit()
    return olsFit

def summStat(r):
    print(r.summary())
    return

def descrStats(data):
    descr = smstats.descriptivestats.describe(data)
    return descr

def test():
    d = [1,2,3,4,5,6,7,8,9,10]
    d1 = [10,9,8,7,6,5,4,3,2,1]
    dataframe = {'X':d,"y":d1}
    df = pd.DataFrame(dataframe)
    fit = leastSquares(d, d1)
    summStat(fit)
    descriptions = descrStats(df)
    print(descriptions)
    
test()