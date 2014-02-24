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

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        context.teach(parts_of_speech = p)

        # @TODO Might need to finish this

    def test_teach_words(self):
        context = knowledge.Knowledge()

        tokenizer = pos.Tokenizer('/')
        tokens = tokenizer.tokenize(self.corpus)
        data = pos.create_from_tokens(tokens)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        context.teach(w)

        self.assertEqual(len(context._words), 8)
        self.assertEqual(context._words['un'].occurence, 2)
        self.assertEqual(context._words['un']._being[p['Det']['Art']], 2)

        # Try to import it again to see if values has correctly changed
        context.teach(w)

        self.assertEqual(len(context._words), 8)
        self.assertEqual(context._words['un'].occurence, 4)
        self.assertEqual(context._words['un']._being[p['Det']['Art']], 4)

        # And check with another corpus
        tokens = tokenizer.tokenize(self.other_corpus)
        data = pos.create_from_tokens(tokens)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        context.teach(w)

        self.assertEqual(len(context._words), 9)
        self.assertEqual(context._words['un'].occurence, 5)
        # @TODO Will work with context._parts_of_speech
        # self.assertEqual(context._words['un']._being[p['Det']['Art']], 5)