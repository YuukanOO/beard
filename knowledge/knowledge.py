class Knowledge:
    """
    Represents a knowledge structure, a context. Contains each word, part of speech tags
    and commands for a particular context.
    """
    
    def __init__(self):
        self._words = {}
        self._parts_of_speech = {}
        
    def teach(self, words={}, parts_of_speech={}):
        """
        Teach this context with given words and/or parts_of_speech.
        This is the main method to train the context.
        """