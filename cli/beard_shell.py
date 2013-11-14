import cmd
import pos
import knowledge
import glob

class BeardShell(cmd.Cmd):
    intro = 'Welcome to the Beard shell.   Type help or ? to list commands.\n'
    prompt = 'beard> '
    
    def __init__(self):
        super(BeardShell, self).__init__()
        
        self.tokenizer = pos.Tokenizer('/')
        self.context = knowledge.Knowledge()
    
    def preloop(self):
        self._load_default_corpus()
    
    def _load_default_corpus(self, lang='fr'):
        for f in glob.glob('data/corpus/%s*.corpus' % lang):
            print('loading : %s ... ' % f, end='')
            tokens = self.tokenizer.tokenize_from_file(f)
            data = pos.create_from_tokens(tokens)
            print('successfuly loaded %s words and %s parts of speech!' 
                  % (len(data.get('words', {})), len(data.get('poss', {}))))
            # TODO Load tose data in the knowledge context
    
    def do_t(self, arg):
        'ONLY FOR TESTS!'
        tokens = self.tokenizer.tokenize_from_file('data/corpus/fr.corpus')
        print(tokens)
        poss = pos.create_from_tokens(tokens)
        print(poss)
    
    def do_bye(self, arg):
        'Exit the Beard shell'
        print('See Ya!')
        return True