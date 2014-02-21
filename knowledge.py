class Knowledge:
    """
    Represents a knowledge structure, a context. Contains each word, part of speech tags
    and commands for a particular context.
    """
    
    def __init__(self):
        self._words = {}
        self._parts_of_speech = {}
        
    def teach(self, words = {}, parts_of_speech = {}):
        """
        Teach this context with given words and/or parts_of_speech.
        This is the main method to train the context.
        """

class Word:
    """
    Represents a word (problem?).
    """
    
    def __init__(self, value, occurence = 1):
        self.value = value
        self.occurence = occurence
        self._being = {}
        
    def being_a(self, pos_obj):
        """
        Gets the emission probability of this word
        to be the given PartOfSpeech object.
        """
        
        if pos_obj not in self._being:
            return 0.0
        
        return self._being[pos_obj] / self.occurence