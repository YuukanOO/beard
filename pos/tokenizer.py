import codecs, re

class Tokenizer:
    
    def __init__(self, delimiter='/'):
        self.delimiter = delimiter
    
    def tokenize_from_file(self, filepath, encoding='utf-8'):
        """
        Tokenize a corpus from a given filepath.
        """
        
        try:
            f = codecs.open(filepath, encoding=encoding)
            with f as content_file:
                content = content_file.read()
            return self.tokenize(content)
        except:
            return False
        
    def tokenize(self, string):
        """
        Tokenize the given string and return a list of tuples [(word, raw_pos)]
        """

        string = re.sub('[.]+', ' .', string)
        string = re.sub('[?]+', ' ?', string)
        string = re.sub('[!]+', ' !', string)
        string = re.sub('[\n\r,]+', ' ', string)
        return [tuple(token.split(self.delimiter)) for token in re.split('[ -]+', string)]