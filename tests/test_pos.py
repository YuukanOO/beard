import unittest
import pos

class TestPartOfSpeech(unittest.TestCase):
    
    string = "Un/Det:Art chat/Nom mange/Ver:Pres une/Det:Art souris/Nom./Punc Un/Det:Art garçon/Nom sourit/Ver:Pres./Punc"

    def test_create_from_tokens(self):
        
        tokenizer = pos.Tokenizer('/')
        tokens = tokenizer.tokenize(self.string)
        data = pos.create_from_tokens(tokens)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        self.assertTrue(w)
        self.assertTrue(p)

        self.assertEqual(len(w), 8)
        self.assertEqual(len(p), 5) # Don't forget the None Pos (start of paragraph)

    def test_part_of_speech_properties(self):
        
        tokens = pos.Tokenizer('/').tokenize(self.string)
        data = pos.create_from_tokens(tokens)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        name_pos = p['Nom']

        self.assertEqual(name_pos.occurence, 3)
        self.assertEqual(name_pos.value, 'Nom')
        self.assertIsNone(name_pos.parent)

        pres_verb_pos = p['Ver']['Pres']
        self.assertEqual(pres_verb_pos.occurence, 2)
        self.assertEqual(pres_verb_pos.value, 'Pres')
        self.assertIsNotNone(pres_verb_pos.parent)
        self.assertEqual(pres_verb_pos.parent, 'Ver')

    def test_part_of_speech_probabilities(self):

        tokens = pos.Tokenizer('/').tokenize(self.string)
        data = pos.create_from_tokens(tokens)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        name_pos = p['Nom']
        article_pos = p['Det']['Art']
        pres_verb_pos = p['Ver']['Pres']

        self.assertEqual(name_pos.being_after(article_pos), 1)
        self.assertAlmostEqual(name_pos.being_before(pres_verb_pos), 0.6666, 3)

        # Not yet implemented
        verb_pos = p['Ver']
        self.assertAlmostEqual(name_pos.being_before(verb_pos), 0.6666, 3)
