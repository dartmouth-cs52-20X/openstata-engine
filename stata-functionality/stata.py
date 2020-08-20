# Stata module
#   a python implementation of Stata commands
#   see READEME.md in this directory for usage
# 
# Arjun Srinivasan, 08-13-2020
# 
import pandas as pd
import numpy as np
import econtools.metrics as mt
from econtools import read
import urllib.request
import os

class Stata:

    def __init__(self):
        self.memory_df = None
        self.subset_df = None

        pd.set_option('display.max_columns', 500)

    # I. Loading and clearing data in memory:
    def clear(self):
        self.memory_df = pd.DataFrame({'A' : []})
        return 0,""

    def use(self, fp, isUrl=False):
        # if not isUrl:
        fname,ftype = os.path.splitext(fp)
        # print("filename:", fname)
        # print("filetype:", ftype)
        if ftype=='.dta' or ftype=='.csv' or ftype=='.pkl' or ftype=='.hdf':
            try:
                df = read(fp)
            except:
                return 1, "Error: Could not load from data file {}".format(fp)
            self.memory_df = df
            return 0, "Loaded {}".format(fp)
        # elif ftype=='.csv':
            # return self.load_csv(fp)
        # elif ftype=='.xlsx':
            # return self.load_xls(fp)
        # elif ftype=='.xls':
            # return self.import_excel(fp)
        else:
            return 0, "Error: Could not read from file format {}".format(ftype)

    # def import_excel(self, fp, isUrl=False):

        # if isUrl:

    # def export_excel(self, fp):

    # def load_csv(self, csv_fp, isUrl=False):
    #     if not isUrl:
    #         try:
    #             df = pd.read_csv(csv_fp)
    #         except error:
    #             return 1, "Error: No csv {}".format(csv_fp)

    # def load_stata(self, dta_fp, isUrl=False):
    #     # if isUrl:
    #     try:
    #         df = pd.read_stata(dta_fp)
    #     except error:
    #         return 1, "Error: No data file {}".format(dta_fp)
    #     self.memory_df = df
    #     return 0



    # II. Basic descriptive statistics commands: summ, desc, mean, log using, 

    # def summarize(self, varlist, ifCondition=None):

    def describe(self, varlist=None, ifCondition=None):

        if varlist==None:
            temp = self.memory_df
        else:
            temp = self.subset_by_varlist(varlist)

            if temp[0] == 1:
                return temp

        try:
            result = temp.describe(include='all')
        except: 
            return 1, "Error: Could not describe data."
        return 0, result


    def mean(self, varlist=None, ifCondition=None):
        if varlist==None:
            return 1, "Error: No varlist."
            # temp = self.memory_df
        else:
            temp = self.subset_by_varlist(varlist)

            if temp[0] == 1:
                return temp

        print(temp[1].head())

        try:
            result = temp[1].mean(axis=0, numeric_only=True)
        except: 
            return 1, "Error: Could not calculate mean."
        return 0, result

    # def log_using(self, fp)

    def subset_by_varlist(self, varlist):

        # cs_varlist = ", ".join(varlist)
        try:
            temp = self.memory_df[varlist]
        except:
            return 1, "Error: Variable in varlist not found."
        return 0, temp

    # III. Basic data transformation commands:
    # def generate(self, varname, varcmd, ifCondition=None)


    def reg(self, y, xs, ifCondition=None):
        try:
            results = mt.reg(self.memory_df, y, xs, addcons=True)
        except:
            return 1, "Error:"
        return 0, results

    # def predict(self, reg_string):


    # def test(self, reg_string):
    
    
    # def merge():


    # Advanced commands: ivreg, areg, forval, foreach, testparm
    # def ivreg():





    # debugging
    def debug_head(self):
        return self.memory_df.head()

