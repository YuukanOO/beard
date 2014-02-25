import unittest
import pos
import knowledge

class TestKnowledge(unittest.TestCase):

    corpus = "Un/Det:Art chat/Nom mange/Ver:Pres une/Det:Art souris/Nom./Punc Un/Det:Art garçon/Nom sourit/Ver:Pres./Punc"
    other_corpus = "Un/Det:Art chameau/Nom mange/Ver:Pres./Punc"

    def test_teach_parts_of_speech(self):
        context = knowledge.Knowledge()

        tokenizer = pos.Tokenizer('/')
        tokens = tokenizer.tokenize(self.corpus)
        data = pos.create_from_tokens(tokens)

        p = data.get('parts_of_speech', {})

        context.teach(parts_of_speech = p)

        self.assertTrue(context._parts_of_speech['Det'])
        self.assertTrue(context._parts_of_speech['Det']['Art'])
        self.assertEqual(len(context._parts_of_speech), 5)
        self.assertEqual(context._parts_of_speech['Nom'].occurence, 3)
        self.assertEqual(context._parts_of_speech['Det']['Art'].occurence, 3)

        art_pos = context._parts_of_speech['Det']['Art']
        self.assertEqual(context._parts_of_speech['Nom']._before[art_pos], 3)

        context.teach(parts_of_speech = p)
        self.assertEqual(len(context._parts_of_speech), 5)
        self.assertEqual(context._parts_of_speech['Nom'].occurence, 6)
        self.assertEqual(context._parts_of_speech['Nom']._before[art_pos], 6)
        self.assertEqual(context._parts_of_speech['Det']['Art'].occurence, 6)

        # And check with another corpus
        tokens = tokenizer.tokenize(self.other_corpus)
        data = pos.create_from_tokens(tokens)

        p = data.get('parts_of_speech', {})
        context.teach(parts_of_speech = p)
        self.assertEqual(len(context._parts_of_speech), 5)
        self.assertEqual(context._parts_of_speech['Nom'].occurence, 7)
        self.assertEqual(context._parts_of_speech['Nom']._before[art_pos], 7)
        self.assertEqual(context._parts_of_speech['Det']['Art'].occurence, 7)

    def test_teach_words(self):
        context = knowledge.Knowledge()

        tokenizer = pos.Tokenizer('/')
        tokens = tokenizer.tokenize(self.corpus)
        data = pos.create_from_tokens(tokens)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        context.teach(w, p)
        art_pos = context._parts_of_speech['Det']['Art']

        self.assertEqual(len(context._words), 8)
        self.assertEqual(context._words['un'].occurence, 2)
        self.assertEqual(context._words['un']._being[art_pos], 2)

        # Try to import it again to see if values has correctly changed
        context.teach(w, p)

        self.assertEqual(len(context._words), 8)
        self.assertEqual(context._words['un'].occurence, 4)
        self.assertEqual(context._words['un']._being[art_pos], 4)

        # And check with another corpus
        tokens = tokenizer.tokenize(self.other_corpus)
        data = pos.create_from_tokens(tokens)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        context.teach(w, p)

        self.assertEqual(len(context._words), 9)
        self.assertEqual(context._words['un'].occurence, 5)
        self.assertEqual(context._words['un']._being[p['Det']['Art']], 5)