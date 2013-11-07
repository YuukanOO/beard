import cmd
import pos

class BeardShell(cmd.Cmd):
    intro = 'Welcome to the Beard shell.   Type help or ? to list commands.\n'
    prompt = 'beard> '
    
    def __init__(self):
        self.tokenizer = pos.Tokenizer('/')
        super(BeardShell, self).__init__()
    
    def do_t(self, arg):
        'ONLY FOR TESTS!'
        tokens = self.tokenizer.tokenize_from_file('corpus/fr.corpus')
        print(tokens)
        poss = pos.PartOfSpeech.create_from_tokens(tokens)
        print(poss)
    
    def do_bye(self, arg):
        'Exit the Beard shell'
        print('See Ya!')
        return True