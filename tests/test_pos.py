from beard import pos
import base_test
import unittest

class TestPosModule(base_test.RequireTokens):

    def test_create_from_tokens(self):

        data = pos.create_from_tokens(self.tokens_01)

        w = data.get('words', {})
        p = data.get('parts_of_speech', {})

        self.assertTrue(w)
        self.assertTrue(p)

        self.assertEqual(len(w), 14)
        self.assertEqual(len(p), 7) # Don't forget the None Pos (start of paragraph)
