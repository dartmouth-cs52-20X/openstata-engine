# Stata module
#   a python implementation of Stata commands
#   see READEME.md in this directory for usage
# 
# Arjun Srinivasan, 08-24-2020
# 
import pandas as pd
import numpy as np
import econtools.metrics as mt
from econtools import read
import urllib.request
import os
import io
import sys
class Stata:

    def __init__(self):
        self.memory_df = pd.DataFrame({'No data in memory.' : []})
        self.results = None
        self.isLogging = False
        self.allLogs = {}
        self.currentLogName = None
        self.currentLog = []

        pd.set_option('display.max_columns', 500)
        pd.options.mode.chained_assignment = None

    # I. Loading and clearing data in memory:
    def clear(self):
        self.memory_df = pd.DataFrame({'No data in memory.' : []})
        return 0,'Cleared data in memory.'

    def handleLog(self, input):
        try:
            if self.isLogging:
                self.currentLog.append(input)
        except:
            return 1, 'Error in logging: unable to handle logging of commands.'
        return 0,'Added to log.'

    def use(self, fp, name, isUrl=False):
        
        if isUrl:
            if '.dta' in fp:
                ftype='.dta'
            elif '.csv' in fp:
                ftype='.csv'
            elif '.xlsx' in fp:
                ftype='.xlsx'
            elif '.xls' in fp:
                ftype='.xls'
            elif '.pkl' in fp:
                ftype='.pkl'
            elif '.hdf' in fp:
                ftype='.hdf'
            else:
                return 1,'Error in command "use": file type unrecognized.'
        else:
            fname,ftype = os.path.splitext(fp)
        
        if ftype==None:
            return 1,'Error in command "use": file type unrecognized.'
        if name==None:
            return 1,'Error in command "use": no file name provided.'

        if ftype=='.dta':
            try:
                df = pd.read_stata(fp)
                self.memory_df = df
                # print(df.head())
            except:
                return 1, 'Error in command "use": Could not load from data file {}'.format(fp)
            return 0, 'Loaded {}'.format(name)
        elif ftype=='.csv':
            try:
                df = pd.read_csv(fp)
                self.memory_df = df
            except:
                return 1, 'Error in command "use": Could not load from data file {}'.format(fp)
            return 0, 'Loaded {}'.format(name)            
        elif ftype=='.pkl': 
            try:
                df = pd.read_pickle(fp)
                self.memory_df = df
            except:
                return 1, 'Error in command "use": Could not load from data file {}'.format(fp)
            return 0, 'Loaded {}'.format(name)            
        elif ftype=='.hdf':
            try:
                df = pd.read_hdf(fp)
                self.memory_df = df
            except:
                return 1, 'Error in command "use": Could not load from data file {}'.format(fp)
            return 0, 'Loaded {}'.format(name)
        elif ftype=='.xlsx' or ftype=='.xls':
            try:
                df = pd.read_excel(fp)
                self.memory_df = df
            except:
                return 1, 'Error in command "use": Could not load from data file {}'.format(fp)
            return 0, 'Loaded {}'.format(name)            
        else:
            return 0, 'Error in command "use": Could not read from file format {}'.format(ftype)

    # II. Basic descriptive statistics commands: summ, desc, mean, log using, 

    def summarize(self, varlist=None, ifCondition=None):

        if ifCondition!=None:
            temp_1 = self.subset_by_ifcondition(self.memory_df, ifCondition)
            if temp_1[0] == 1:
                return temp_1[1]
            else:
                temp = temp_1[1].copy()
        else:
            temp = self.memory_df

        # if varlist==None or len(varlist)==0:
            # temp = self.memory_df
        if varlist!=None and len(varlist)>0:
            temp = self.subset_by_varlist(temp, varlist, caller="summarize")
            if temp[0] == 1:
                return temp
            else:
                temp = temp[1]

        try:
            # print(temp.head())
            result = temp.describe().to_string()
        except: 
            return 1, 'Error in command "summarize": Could not summarize data.'
        return 0, result

    def describe(self, varlist=None, ifCondition=None):

        # if ifCondition!=None:
        #     temp_1 = self.subset_by_ifcondition(self.memory_df, ifCondition)
        #     if temp_1[0] == 1:
        #         return temp_1[1]
        #     else:
        #         temp = temp_1[1].copy()
        # else:
        #     temp = self.memory_df

        if varlist==None or len(varlist)==0:
            temp = self.memory_df
        else:
            temp = self.subset_by_varlist(self.memory_df, varlist, caller="describe")
            if temp[0] == 1:
                return temp
            else:
                temp = temp[1]

        try:
            buf = io.StringIO()
            temp.info(buf=buf)
            # print('here')
            result = buf.getvalue()
            # print(result)
        except: 
            return 1, 'Error in command "describe": could not describe data.'
        return 0, result

    def mean(self, varlist, ifCondition=None):

        if ifCondition!=None:
            temp_1 = self.subset_by_ifcondition(self.memory_df, ifCondition)
            if temp_1[0] == 1:
                return temp_1[1]
            else:
                temp = temp_1[1].copy()
        else:
            temp = self.memory_df

        if varlist==None or len(varlist)==0:
            return 1, 'Error in command "mean": must have varlist (try: mean var_one var_two).'
        else:
            temp = self.subset_by_varlist(temp, varlist, caller="mean")
            if temp[0] == 1:
                return temp

        try:
            if len(varlist)==1:
                result = temp[1].mean(numeric_only=True).to_string()                
            else:
                result = temp[1].mean(axis=0, numeric_only=True).to_string()
        except:
            return 1, 'Error in command "mean": could not calculate mean.'
        return 0, result

    def log(self, type, fname=None):
        if type=='using':
            if fname==None:
                return 1, 'Error in command "log": no filename provided.'
            elif self.isLogging == True:
                return 1, 'Error in command "log": must close currently open log {} (try: capture log close) before opening new log.'
            else:
                try:
                    self.isLogging = True
                    self.currentLogName = fname
                    self.currentLog = []
                except:
                    return 1, 'Error in command "log": unable to create log file with name {}'.format(fname)
                return 0, 'Log file {} opened.'.format(fname)
        elif type=='close':
            if self.isLogging == False:
                return 1, 'Error in command "log": cannot close when no log file is open.'
            else:
                try:
                    result = self.captureLogClose()
                except:
                    return 1, 'Error in command "log": unable to close the currently open log file.'
                return result
        else:
            return 1, 'Error in command "log": invalid argument (try: log using fname OR try: log close)'

    def captureLogClose(self):
        if self.isLogging==True:
            try:
                if len(self.currentLog) > 0:
                    log = "\n\n".join(self.currentLog)
                else:
                    log = " "               
                self.allLogs[self.currentLogName] = log
                temp = self.currentLogName
                self.currentLogName = None
                self.currentLog = []
                self.isLogging = False
            except :
                return 1, 'Error in command "capture log close" or "log close": unable to close log file.'
            return 0, 'Close log file {}'.format(temp)
        else:
            return 0, 'No log open. Program proceeds.'

    def subset_by_varlist(self, data, varlist, caller):
        # cs_varlist = ", ".join(varlist)
        # add check if the variables are there
        try:
            temp = data[varlist]
        except:
            return 1, 'Error in command "{}": variable in varlist not found.'.format(caller)
        return 0, temp

    def subset_by_ifcondition(self, data, cond):

        try:
            # print(cond)
            # print(data)
            # print(data.head())
            # print("evaluting")
            temp = data.query(cond)
        except:
            return 1, 'Error in if-condition {}: unable to evaluate.'.format(cond)
        return 0, temp

    # III. Basic data transformation commands:
    def generate(self, newvar, expression, ifCondition=None):

        if newvar==None:
            return 1, 'Error in command "generate": no new variable name (try: gen newvar = expression).'
        elif expression==None:
            return 1, 'Error in command "generate": no value for new variable (try: gen newvar = expression).'

        if newvar in self.memory_df.columns:
            return 1, 'Error in command "generate": Variable {} already exists.'.format(newvar)
        # elif ifCondition == None:
        else:
            try:
                self.memory_df[newvar] = self.memory_df.eval(expression)
            except:
                return 1, 'Error in command "generate": could not evaluate expression: {}'.format(expression)
        # else:
        #     try:
        #         status, slice = self.subset_by_ifcondition(self.memory_df, ifCondition)
        #         self.memory_df.loc[slice][newvar] = slice.eval(expression)
        #         print(self.memory_df.head())
        #     except:
        #         return 1, 'Error in command "generate": could not evaluate expression: {}'.format(expression)
        return 0, 'Generated new variable: {}'.format(newvar)


    def replace(self, oldvar, expression, ifCondition=None):

        if oldvar==None:
            return 1, 'Error in command "replace": no old variable name (try: replace oldvar = expression).'
        elif expression==None:
            return 1, 'Error in command "replace": no value for new variable (try: replace oldvar = expression).'

        if oldvar in self.memory_df.columns:
            try:
                self.memory_df[oldvar] = self.memory_df.eval(expression)
            except:
                return 1, 'Error in command "replace": could not evaluate expression: {}'.format(expression)
            return 0, 'Replaced values for variable: {}'.format(oldvar)
        else:
            return 1, 'Error in command "replace": No variable {} in data in memory.'.format(oldvar)

    def rename(self, oldname, newname):

        if oldname==None:
            return 1, 'Error in command "rename": no old variable name (try: rename old_varname new_varname).'
        elif newname==None:
            return 1, 'Error in command "rename": no new variable name (try: rename old_varname new_varname).'

        if oldname in self.memory_df.columns:
            try:
                self.memory_df = self.memory_df.rename(columns={oldname: newname})
            except:
                return 1, 'Error in command "rename": unable to rename variable {} to {}'.format(oldname,newname)
            return 0, 'Renamed variable {} to {}'.format(oldname,newname)
        else:
            return 1, 'Error in command "rename": no variable {} in data in memory.'.format(oldname)

    def drop(self, varlist=None, ifCondition=None):

        if varlist==None and ifCondition==None:
            return 1, 'Error in command "drop": no arguments provided.'
        elif varlist!=None and ifCondition!=None :
            return 1, 'Error in command "drop": cannot conditionally drop variables.'
        elif varlist!=None and ifCondition==None:
            # add check if variables are there
            try:
                self.memory_df  = self.memory_df.drop(columns=varlist)
            except:
                return 1, 'Error in command "drop": could not drop variables {} from data in memory.'.format(varlist)
            return 0, 'Dropped variables {} from data in memory.'.format(varlist)
        else:
            # fill in if condition
            status, self.memory_df = self.subset_by_ifcondition(self.memory_df, 'not ' + ifCondition)
            return 0, 'Rows that did not match condition {} were dropped.'.format(ifCondition)

    def keep(self, varlist=None, ifCondition=None):
        if varlist==None and ifCondition==None:
            return 1, 'Error in command "keep": no arguments provided.'
        elif varlist!=None and ifCondition!=None :
            return 1, 'Error in command "keep": cannot conditionally keep variables.'
        elif varlist!=None and ifCondition==None:
            # add check if variables are there
            try:
                self.memory_df  = self.memory_df[varlist]
            except:
                return 1, 'Error in command "keep": could not keep variables {} from data in memory.'.format(varlist)
            return 0, 'Kept only variables {} from data in memory.'.format(varlist)
        else:
            # fill in if condition
            status, self.memory_df = self.subset_by_ifcondition(self.memory_df, ifCondition)
            return 0, 'Rows matching condition {} were kept.'.format(ifCondition)

    def tabulate(self, var_one, var_two=None, ifCondition=None, gen=None):

        if var_one==None:
            return 1, 'Error in command "tabulate": no variable 1 (try: tab var1)'

        if gen==None:
            
            if var_two==None:

                if var_one not in self.memory_df.columns:
                    return 1, 'Error in command "tabulate": no variable {} in data in memory.'.format(var_one)
                try:
                    result = self.memory_df[var_one].value_counts()
                    d = {'Values': result.index, 'Counts': result.values}
                    # print(result.index)
                    # print(result.values)
                    result_df = pd.DataFrame(data=d)
                    # result.name = "Value - Count"
                except:
                    return 1, 'Error in command "tabulate": unable to get value counts for variable {}'.format(var_one)
                return 0, result_df

            else:
                if var_one not in self.memory_df.columns:
                    return 1, 'Error in command "tabulate": no variable {} in data in memory.'.format(var_one)
                if var_two not in self.memory_df.columns:
                    return 1, 'Error in command "tabulate": no variable {} in data in memory.'.format(var_two)
                try:
                    df = self.memory_df[[var_one, var_two]].copy()
                    # print('here')
                    result = df.count_values()
                    # d = {'Values': result.index, 'Counts': result.values}
                    # print(result.index)
                    # print(result.values)
                    # result_df = pd.DataFrame(data=d)
                    # result.name = "Value - Count"
                except:
                    return 1, 'Error in command "tabulate": unable to get value counts for variables {} and {}'.format(var_one, var_two)
                return 0, result

        else:
            return 1, 'Error in command "tabulate": did not generate variable'

    def reg(self, y, xs, ifCondition=None, vce_type=None, cluster=None):

        if y==None:
            return 1, 'Error in command "regress": no y variable (try: regress y x).'
        elif xs==None:
            return 1, 'Error in command "regress": no x variable(s) (try: regress y x).'
        # use set stuff to check all variables are in df?
        try:
            results = mt.reg(self.memory_df, y, xs, vce_type=vce_type, cluster=cluster, addcons=True)
            self.results = results
            output = results.summary.to_string()
        except:
            return 1, 'Error in command "regress": unable to run.'
        return 0, output

    def predict(self, newvar, option='resid'):
        if newvar==None:
            return 1, 'Error in command "predict": no new variable name (try: predict newvar)'
        elif self.results==None:
            return 1, 'Error in command "predict": must be run after running command "regress"'
        elif newvar in self.memory_df.columns:
            return 1, 'Error in command "predict": variable named {} already exists.'.format(newvar)

        if option=='resid':
            try:
                self.memory_df.loc[self.results.sample, newvar] = self.results.resid
            except:
                return 1, 'Error in command "predict": unable to store regression residuals'
            return 0, 'Stored regression residuals in variable {}'.format(newvar)
        elif option=='xb':
            try:
                self.memory_df.loc[self.results.sample, newvar] = self.results.yhat
            except:
                print(error)
                return 1, 'Error in command "predict": unable to store regression predicted values (xb)'
            return 0, 'Store regression predicted values (xb) in variable {}'.format(newvar)
        else:
            return 1, 'Error in command "predict": unrecognized option: {}'.format(option)

    def test(self, varlist):
        if self.results==None:
            return 1, 'Error in command "test": must be run after running command "regress"'
        elif varlist==None:
            return 1, 'Error in command "test": no variables to test (try: test var1 var2)'

        try:
            result_tuple = self.results.Ftest(varlist)
            result = "F-stat: {}, p-score for F: {}".format(result_tuple[0], result_tuple[1])
        except:
            return 1, 'Error in command "test": unable to perform F test with variables {}'.format(varlist)
        return 0, result
    
    # def merge():
    # Advanced commands: ivreg, areg, forval, foreach, testparm
    # debugging
    def debug_head(self):
        return self.memory_df.head()

