import sys

sys.path.append("./stata-functionality/")
from stata import Stata

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
            except:
                result_list.append('No input for commad {}'.format(i))
                break
            
            cmd_output = self.run_command(do_file[i])       # run the command
            result_list.append(cmd_output[1])               # add the output
            if (cmd_output[0] == 1):
                break                                       # break on error

        return result_list

    def run_command(self, command):

        try:
            cmd = command['command']
        except:
            return 1, "Error: No command name in parsed command."

        print(cmd)
        if cmd=='clear':
            result = self.stata.clear()
            return result
        elif cmd=='use':
            try:
                fp = command['args'][0]
            except:
                return 1, "Error: No filepath in parsed command: use"
            result = self.stata.use(fp, isUrl=True)
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
            print(result)
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
        # elif cmd=='log':

        # elif cmd=='capture log close':

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

    









