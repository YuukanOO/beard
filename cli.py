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
            w = data.get('words', {})
            p = data.get('parts_of_speech', {})
            print('successfuly loaded %s words and %s parts of speech!' 
                  % (len(w), len(p)))
            self.context.teach(w, p)
    
    def do_bye(self, arg):
        'Exit the Beard shell'
        print('See Ya!')
        return True