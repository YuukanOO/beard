import unittest
import pos
import os

class TestTokenizer(unittest.TestCase):
    
    def setUp(self):
        self.tokenizer = pos.Tokenizer('/')

    def test_tokenize(self):
        string = "Un/Det:Art chat/Nom mange/Ver:Pres une/Det:Art souris/Nom./Punc"
        
        tokens = self.tokenizer.tokenize(string)
        
        self.assertEqual(len(tokens), 6)
        
        w, p = tokens[2]
        self.assertEqual(w, 'mange')
        self.assertEqual(p, 'Ver:Pres')

    def test_tokenize_from_file(self):

        tokens = self.tokenizer.tokenize_from_file(os.path.dirname(__file__) + '/sample_01.corpus')

        self.assertTrue(tokens)
        self.assertEqual(len(tokens), 25)

        w, p = tokens[2]
        self.assertEqual(w, 'est')
        self.assertEqual(p, 'Ver:Pres')