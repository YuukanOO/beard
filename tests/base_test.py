from beard import pos
import unittest
import os

class RequireTokens(unittest.TestCase):
    """
    Represents a test which needs Tokens to work correctly.
    """

    def setUp(self):
        super(RequireTokens, self).setUp()
        self.tokenizer = pos.Tokenizer('/')
        self.tokens_01 = self.tokenizer.tokenize_from_file(os.path.dirname(__file__) + '/sample_01.corpus')
        self.tokens_02 = self.tokenizer.tokenize_from_file(os.path.dirname(__file__) + '/sample_02.corpus')

class RequireDatas(RequireTokens):
    """
    Represents a test which needs data (ie. PartOfSpeechs + Words) to work.
    """

    def setUp(self):
        super(RequireDatas, self).setUp()
        self.datas_01 = pos.create_from_tokens(self.tokens_01)
        self.words_01 = self.datas_01.get('words', {})
        self.pos_01 = self.datas_01.get('parts_of_speech', {})

        self.datas_02 = pos.create_from_tokens(self.tokens_02)
        self.words_02 = self.datas_02.get('words', {})
        self.pos_02 = self.datas_02.get('parts_of_speech', {})        