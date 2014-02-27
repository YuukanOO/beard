import base_test
import unittest
import pos

class TestPartOfSpeech(base_test.RequireDatas):

    def test_part_of_speech_properties(self):

        w, p = self.words_01, self.pos_01

        name_pos = p['Nom']
        pres_verb_pos = p['Ver']['Pres']

        self.assertEqual(name_pos.occurence, 7)
        self.assertEqual(name_pos.value, 'Nom')
        self.assertIsNone(name_pos.parent)

        self.assertEqual(pres_verb_pos.occurence, 2)
        self.assertEqual(pres_verb_pos.value, 'Pres')
        self.assertIsNotNone(pres_verb_pos.parent)
        self.assertEqual(pres_verb_pos.parent, 'Ver')

    def test_part_of_speech_probabilities(self):

        w, p = self.words_01, self.pos_01

        name_pos = p['Nom']
        verb_pos = p['Ver']
        article_pos = p['Det']['Art']
        pres_verb_pos = p['Ver']['Pres']

        self.assertAlmostEqual(name_pos.being_after(article_pos), 0.7142, 3)
        self.assertAlmostEqual(name_pos.being_before(pres_verb_pos), 0.2857, 3)
        self.assertAlmostEqual(name_pos.being_before(verb_pos), 0.4285, 3)

        w, p = self.words_02, self.pos_02

        name_pos = p['Nom']
        verb_pos = p['Ver']
        article_pos = p['Det']['Art']
        pres_verb_pos = p['Ver']['Pres']

        self.assertEqual(name_pos.being_after(article_pos), 1)
        self.assertAlmostEqual(name_pos.being_before(pres_verb_pos), 0.6666, 3)
        self.assertAlmostEqual(name_pos.being_before(verb_pos), 0.6666, 3)