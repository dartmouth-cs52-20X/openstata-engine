import sys

sys.path.append("./stata-functionality/")
from stata import Stata

def handleTutorials(tid, do_f):

    if tid==None or do_f==None:
        return 1, 'Cannot grade tutorial: no tutorial nubmer or program output'
    else:
        try:
            if tid=='tutorial_01':
                try:
                    k = len(do_f)
                    if do_f[k-1]['command'] == "summarize" and do_f[k-2]['command'] == "describe" and do_f[k-2]['args'] == ["sex"]:
                        return 0,"Tutorial Passed!"
                    else:
                        return 0,"Tutorial failed. Try again!"
                except:
                    return 0,"Tutorial failed. Try again!"
            elif tid=='tutorial_02':
                k = len(do_f)
                try:
                    if do_f[k-1]['command'] == "capture log close" and do_f[k-2]['command'] == "summarize" and do_f[k-3]['command'] == "log" and do_f[k-3]['args'][0] == "using" and do_f[k-3]['args'][1] == "tutorial-two":
                        return 0,"Tutorial Passed!"
                    else:
                        return 0,"Tutorial failed. Try again!"
                except:
                    return 0,"Tutorial failed. Try again!"
            elif tid=='tutorial_03':
                k = len(do_f)
                try:
                    if do_f[k-1]['command'] == "capture log close" and do_f[k-2]['command'] == "regress" and do_f[k-3]['command'] == "generate" and do_f[k-4]['command'] == "log":
                        if do_f[k-2]['args'][0] == "wage_hr" and ((do_f[k-2]['args'][1][0] == "age" and do_f[k-2]['args'][1][1] == "age2") or (do_f[k-2]['args'][1][0] == "age2" and do_f[k-2]['args'][1][1] == "age")):
                            if do_f[k-3]['args'][0] == "age2" and (do_f[k-3]['args'][1] == "age**2" or do_f[k-3]['args'][1] == "age*age"):
                                if do_f[k-4]['args'][0] == "using" and do_f[k-4]['args'][1] == "tutorial-three":
                                    return 0,"Tutorial Passed!"
                                else:
                                    return 0, "Tutorial failed. Incorrect log using command."
                            else:
                                return 0, "Tutorial failed. Incorrectly generated age2. Try again!"
                        else:
                            return 0, "Tutorial failed. Incorrect regression. Try again!"
                    else:
                        return 0,"Tutorial failed. Missing/incorrect command Try again!"
                except:
                    return 0,"Tutorial failed. Try again!"
            else:
                return 1, 'Unrecognized tutorial!'

        except:
            return 1, 'Cannot grade tutorial. Sorry!'

class RunStata:

    def __init__(self):
        self.placeholder = 0
        self.stata = Stata()

    def run_do_file(self, do_file):

        num_cmds = len(do_file)                             # number of commands
        result_list = []                                    # list to hold interspered input and output

        for i in range(0, num_cmds):                        # for each command

            try:
                result_list.append(do_file[i]['input'])         # add raw command text
                ret = self.stata.handleLog(do_file[i]['input'])
            except:
                result_list.append('No input for commad {}'.format(i))
                break
            
            cmd_output = self.run_command(do_file[i])       # run the command
            # print(cmd_output)
            ret = self.stata.handleLog(cmd_output[1])
            result_list.append(cmd_output[1])               # add the output
            if (ret[0] == 1):
                break
            if (cmd_output[0] == 1):
                closetry = self.stata.captureLogClose()
                break                                       # break on error

        logs = self.stata.allLogs
        return result_list, logs

    def run_command(self, command):

        try:
            cmd = command['command']
        except:
            return 1, "Error: No command name in parsed command."

        # print(cmd)
        if cmd=='clear':
            result = self.stata.clear()
            return result
        elif cmd=='use':
            try:
                fp = command['args'][0]
                name = command['args'][1]
            except:
                return 1, "Error: No filepath and/or filename in parsed command: use"
            result = self.stata.use(fp, name, isUrl=True)
            return result
        elif cmd=='summarize':
            try:
                varlist = command['args']
                ifcon = command['condition']
            except:
                return 1, "Error: Missing arguments or condition in parsed command: summarize"
            result = self.stata.summarize(varlist=varlist,ifCondition=ifcon)
            return result
        elif cmd=='describe':
            try:
                varlist = command['args']
            except:
                return 1, "Error: Missing arguments in parsed command: summarize"
            result = self.stata.describe(varlist=varlist)
            # print(result)
            return result
        elif cmd=='mean':
            try:
                varlist = command['args']
                ifcon = command['condition']
            except:
                return 1, "Error: Missing arguments or condition in parsed command: mean"
            if len(varlist)==0:
                return 1, "Error: Empty varlist in parsed command: mean"
            result = self.stata.mean(varlist=varlist,ifCondition=ifcon)
            return result
        elif cmd=='log':
            try:
                type = command['args'][0]
                if len(command['args'])==2:
                    fname = command['args'][1]
                else:
                    fname = None
            except:
                return 1, "Error: Missing arguments in parsed command: log"
            result = self.stata.log(type=type, fname=fname)
            return result
        elif cmd=='capture log close':
            result = self.stata.captureLogClose()
            return result
        elif cmd=='generate':
            try:
                newvar = command['args'][0]
                expression = command['args'][1]
                ifcon = command['condition']
            except:
                return 1, "Error: Missing arguments or expression in parsed command: generate"
            result = self.stata.generate(newvar=newvar, expression=expression,ifCondition=ifcon)
            return result
        elif cmd=='replace':
            try:
                oldvar = command['args'][0]
                expression = command['args'][1]
                ifcon = command['condition']
            except:
                return 1, "Error: Missing arguments or expression in parsed command: replace"
            result = self.stata.replace(oldvar=oldvar, expression=expression,ifCondition=ifcon)
            return result
        elif cmd=='rename':
            try:
                oldname = command['args'][0]
                newname = command['args'][1]
            except:
                return 1, "Error: Missing arguments or expression in parsed command: drop"
            result = self.stata.rename(oldname=oldname,newname=newname)
            return result
        elif cmd=='drop':
            try:
                varlist = command['args']
                ifcon = command['condition']
            except:
                return 1, "Error: Missing arguments or expression in parsed command: drop"
            result = self.stata.drop(varlist=varlist,ifCondition=ifcon)
            return result
        elif cmd=='keep':
            try:
                varlist = command['args']
                ifcon = command['condition']
            except:
                return 1, "Error: Missing arguments or expression in parsed command: drop"
            result = self.stata.drop(varlist=varlist,ifCondition=ifcon)
            return result
        # elif cmd=='tabulate':

        # elif cmd=='merge':

        elif cmd=='regress':
            try:
                y = command['args'][0]
                xs = command['args'][1]
                ifcon = command['condition']
            except:
                return 1, "Error: Missing arguments or expression in parsed command: drop"
            result = self.stata.reg(y=y,xs=xs,ifCondition=ifcon)
            return result
        # elif cmd=='predict':
        # elif cmd=='test':
        # elif cmd=='summarize'
        # elif cmd=='summarize'
        # elif cmd=='summarize'
        # elif cmd=='summarize'
        # elif cmd=='summarize'
        # elif cmd=='summarize'
        # elif cmd=='summarize'
        # elif cmd=='summarize'
        else:
            return 1, "Error: Unrecognized command name: {}".format(cmd)
