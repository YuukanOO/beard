import unittest
import pos

class TestTokenizer(unittest.TestCase):
    
    def test_tokenize(self):
        string = "Un/Det:Art chat/Nom mange/Ver:Pres une/Det:Art souris/Nom./Punc"
        
        tokenizer = pos.Tokenizer('/')
        tokens = tokenizer.tokenize(string)
        
        self.assertEqual(len(tokens), 6)
        
        w, p = tokens[2]
        self.assertEqual(w, 'mange')
        self.assertEqual(p, 'Ver:Pres')