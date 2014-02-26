import unittest
import pos
import os

class RequireTokens(unittest.TestCase):
    """
    Represents a test which needs Tokens to work correctly.
    """

    def setUp(self):
        super(RequireTokens, self).setUp()
        self.tokenizer = pos.Tokenizer('/')
        self.tokens_01 = self.tokenizer.tokenize_from_file(os.path.dirname(__file__) + '/sample_01.corpus')

class RequireDatas(RequireTokens):
    """
    Represents a test which needs data (ie. PartOfSpeechs + Words) to work.
    """

    def setUp(self):
        super(RequireDatas, self).setUp()
        self.data_01 = pos.create_from_tokens(self.tokens_01)