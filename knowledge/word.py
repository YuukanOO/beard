class Word:
    """
    Represents a word (problem?).
    """
    
    def __init__(self, value, occurence=1):
        self.value = value
        self.occurence = occurence
        self.being = {}
        
    def being_a(self, pos_obj):
        """
        Gets the emission probability of this word
        to be the given PartOfSpeech object.
        """
        
        if pos_obj not in self.being:
            return 0.0
        
        return self.being[pos_obj] / self.occurence