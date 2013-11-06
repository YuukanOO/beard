import cmd

class BeardShell(cmd.Cmd):
    intro = 'Welcome to the Beard shell.   Type help or ? to list commands.\n'
    prompt = 'beard> '
    
    def do_bye(self, arg):
        'Exit the Beard shell'
        print('See Ya!')
        return True