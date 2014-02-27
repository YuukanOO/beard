from beard import knowledge
import base_test
import unittest

class TestKnowledge(base_test.RequireDatas):  

    def test_teach_parts_of_speech(self):
        context = knowledge.Knowledge()

        p = self.pos_01
        art_pos = p['Det']['Art']

        context.teach_parts_of_speech(p)

        self.assertTrue(context._parts_of_speech['Det'])
        self.assertTrue(context._parts_of_speech['Det']['Art'])
        self.assertEqual(len(context._parts_of_speech), 7)
        self.assertEqual(context._parts_of_speech['Nom'].occurence, 7)
        self.assertEqual(context._parts_of_speech['Det']['Art'].occurence, 5)
        self.assertEqual(context._parts_of_speech['Nom']._before[art_pos], 5)

        context.teach_parts_of_speech(p)
        self.assertEqual(len(context._parts_of_speech), 7)
        self.assertEqual(context._parts_of_speech['Nom'].occurence, 14)
        self.assertEqual(context._parts_of_speech['Det']['Art'].occurence, 10)
        self.assertEqual(context._parts_of_speech['Nom']._before[art_pos], 10)

        # And check with another corpus
        p = self.pos_02

        context.teach_parts_of_speech(p)

        self.assertEqual(len(context._parts_of_speech), 7)
        self.assertEqual(context._parts_of_speech['Nom'].occurence, 17)
        self.assertEqual(context._parts_of_speech['Det']['Art'].occurence, 13)
        self.assertEqual(context._parts_of_speech['Nom']._before[art_pos], 13)

    def test_teach_words(self):
        context = knowledge.Knowledge()

        w, p = self.words_01, self.pos_01
        art_pos = p['Det']['Art']
        name_pos = p['Nom']

        context.teach_words(w)

        self.assertEqual(len(context._words), 14)
        self.assertEqual(context._words['son'].occurence, 4)
        self.assertEqual(context._words['son']._being[name_pos], 3)

        # Try to import it again to see if values has correctly changed
        context.teach_words(w)

        self.assertEqual(len(context._words), 14)
        self.assertEqual(context._words['son'].occurence, 8)
        self.assertEqual(context._words['son']._being[name_pos], 6)

        # And check with another corpus
        w, p = self.words_02, self.pos_02

        context.teach_words(w)

        self.assertEqual(len(context._words), 20)
        self.assertEqual(context._words['un'].occurence, 2)
        self.assertEqual(context._words['un']._being[p['Det']['Art']], 2)