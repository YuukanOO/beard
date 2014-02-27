import base_test
import unittest

class TestWord(base_test.RequireDatas):

    def test_word_properties(self):

        p, w = self.pos_01, self.words_01

        word = w['son']
        word_raise = w['monte']
        name_pos = p['Nom']
        det_pos_pos = p['Det']['Pos']
        verb_pres_pos = p['Ver']['Pres']
        verb_imp_pos = p['Ver']['Impe']

        self.assertEqual(word.occurence, 4)
        self.assertEqual(word._being[name_pos], 3)
        self.assertEqual(word._being[det_pos_pos], 1)

        self.assertEqual(word_raise.occurence, 2)
        self.assertEqual(word_raise._being[verb_pres_pos], 1)
        self.assertEqual(word_raise._being[verb_imp_pos], 1)        

    def test_word_probabilities(self):

        p, w = self.pos_01, self.words_01

        word = w['son']
        name_pos = p['Nom']
        det_pos = p['Det']
        det_pos_pos = p['Det']['Pos']

        self.assertEqual(word.being_a(name_pos), 0.75)
        self.assertEqual(word.being_a(det_pos_pos), 0.25)
        self.assertEqual(word.being_a(det_pos), 0.25)

        p, w = self.pos_02, self.words_02

        word = w['un']
        name_pos = p['Nom']
        det_pos = p['Det']
        det_art_pos = p['Det']['Art']

        self.assertEqual(word.being_a(name_pos), 0)
        self.assertEqual(word.being_a(det_art_pos), 1)
        self.assertEqual(word.being_a(det_pos), 1)