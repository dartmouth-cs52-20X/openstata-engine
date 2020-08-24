

class RunStata:

    def __init__(self):
        self.placeholder = 0

    def run_do_file(self, do_file):

        num_cmds = len(do_file)                             # number of commands
        result_list = []                                    # list to hold interspered input and output

        for i in range(0, num_cmds):                        # for each command

            result_list.append(do_file[i]['input'])         # add raw command text
            cmd_output = self.run_command(do_file[i])       # run the command
            result_list.append(cmd_output[1])               # add the output
            if (cmd_output[0] == 1):
                break                                       # break on error

        return result_list

    def run_command(self, command):

        try:
            cmd = command['command']
        except:
            return 1, "Error: No command name."

        if cmd=='clear':
            return 0,"Clear worked."
        # elif cmd=='use':

        # elif cmd=='summarize':

        # elif cmd=='describe':

        # elif cmd=='mean':

        # elif cmd=='log':

        # elif cmd=='capture log close':

        # elif cmd=='generate':

        # elif cmd=='replace':

        # elif cmd=='rename':

        # elif cmd=='drop':

        # elif cmd=='keep':

        # elif cmd=='tabulate':

        # elif cmd=='merge':

        # elif cmd=='regress':

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

    









