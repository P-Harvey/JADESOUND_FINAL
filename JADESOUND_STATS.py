# JADESOUND FP
# 20211207

import numpy as np
import scipy as sp
import statsmodels as sm

def leastSquares(X, y):
    olsFit = sm.OLS(y, X).fit()
    return olsFit

def summStat(r):
    print(r.summary())
    return

