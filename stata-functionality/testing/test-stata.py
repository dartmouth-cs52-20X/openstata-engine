# Test of stata.py module and methods
#
# Arjun Srinivasan, 08-13-2020
# 
import pandas as pd
import numpy as np
import econtools.metrics as mt
import sys
import os

sys.path.append("..")
from stata import Stata

def main():

    # constants passed into the stata methods
    my_dta = "./data/cpsmar08_10pct.dta" 
    url_csv = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv'
    url_dta = 'https://github.com/arjunsrini/open-stata-data/blob/master/cpsmar08_10pct.dta?raw=true'
    url_xlsx = 'https://covid.ourworldindata.org/data/owid-covid-data.xlsx'

    print("----------------------------------------------------------------------------------")
    print("Testing Stata.py functionality!")
    print("----------------------------------------------------------------------------------")

    print("----------------------------------------------------------------------------------")
    print("Initialize Stata object:")
    print("----------------------------------------------------------------------------------")
    stata = Stata()

    print("----------------------------------------------------------------------------------")
    print("Testing: Use (x2)")
    print("----------------------------------------------------------------------------------")
    result = stata.use(my_dta, isUrl=True)
    print("Result:", result[1])

    # result = stata.use(url_csv, isUrl=True)
    # print("Result:", result[1])

    # result = stata.use(url_xlsx, isUrl=True)
    # print("Result:", result[1])

    # print("----------------------------------------------------------------------------------")
    # print("Testing: clear")
    # print("----------------------------------------------------------------------------------")
    # result = stata.clear()
    # print("Result:", result[1])

    # print("----------------------------------------------------------------------------------")
    # print("Testing: Use ")
    # print("----------------------------------------------------------------------------------")
    # result = stata.use(url_dta, isUrl=True)
    # print("Result:", result[1])

    # print("----------------------------------------------------------------------------------")
    # print("Debug: show head of data in memory")
    # print("----------------------------------------------------------------------------------")
    # result = stata.debug_head()
    # print(result)

    print("----------------------------------------------------------------------------------")
    print("Testing: Summarize")
    print("----------------------------------------------------------------------------------")
    result = stata.summarize()
    print("Result:", result[1])

    result = stata.summarize(varlist=['age', 'hhid'])
    print("Result:", result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Describe")
    print("----------------------------------------------------------------------------------")
    result = stata.describe()
    print("Result:", result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Describe with varlist")
    print("----------------------------------------------------------------------------------")
    result = stata.describe(varlist=['age', 'hhid'])
    print("Result:", result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Mean")
    print("----------------------------------------------------------------------------------")
    result = stata.mean(['age', 'hhid'])
    print(result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Generate")
    print("----------------------------------------------------------------------------------")
    result = stata.generate('age2', 'age**2')
    print(result[1])

    print("----------------------------------------------------------------------------------")
    result = stata.summarize(['age','age2'])
    print(result[1])


    print("----------------------------------------------------------------------------------")
    print("Testing: Regress")
    print("----------------------------------------------------------------------------------")
    result = stata.reg('wage_hr',['hhid', 'age', 'age2'])
    print(result[1])
    result = stata.reg('wage_hr',['hhid', 'age', 'age2'], vce_type='cluster', cluster='age')
    print(result[1])
    result = stata.reg('wage_hr',['hhid', 'age', 'age2'], vce_type='robust')
    print(result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Predict")
    print("----------------------------------------------------------------------------------")    
    result = stata.predict('myresids')
    print(result[1])
    result = stata.predict('mypredicts', option='xb')
    print(result[1])

    print("----------------------------------------------------------------------------------")
    result = stata.summarize(['myresids','mypredicts'])
    print(result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Test")
    print("----------------------------------------------------------------------------------")    
    result = stata.test(['age'])
    print(result[1])

    result = stata.test(['age', 'age2'])
    print(result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Tabulate")
    print("----------------------------------------------------------------------------------")    
    result = stata.tabulate('age')
    print(result[1])
    
    # result = stata.tabulate('age', 'sex')
    # print(result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Replace")
    print("----------------------------------------------------------------------------------")
    result = stata.replace('age2', '1')
    print(result[1])

    print("----------------------------------------------------------------------------------")
    result = stata.summarize(['age','age2'])
    print(result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Rename")
    print("----------------------------------------------------------------------------------")
    result = stata.rename('age2', 'age_squared')
    print(result[1])

    print("----------------------------------------------------------------------------------")
    result = stata.summarize(['age','age_squared'])
    print(result[1])

    print("----------------------------------------------------------------------------------")
    print("Testing: Drop")
    print("----------------------------------------------------------------------------------")    
    result = stata.drop('age')
    print(result[1])

    print("----------------------------------------------------------------------------------")
    result = stata.summarize(['age'])
    print(result[1])

if __name__ == "__main__":
    main()