import pos

class Knowledge:
    """
    Represents a knowledge structure, a context. Contains each word, part of speech tags
    and commands for a particular context.
    """
    
    def __init__(self):
        self._words = {}
        self._parts_of_speech = {}
        
    def teach_parts_of_speech(self, poss, look_in = None):
        """
        Recursively process Part of SpeechS to adjust knowledge probabilities.
        """

        look_in = look_in or self._parts_of_speech

        for raw, val in poss.items():
            if raw in look_in:
                if type(val) is dict:
                    self.teach_parts_of_speech(val, look_in[raw])
                else:
                    k_pos = look_in[raw]
                    k_pos.occurence += val.occurence
                    # Process before probabilities
                    for pos, occurence in val._before.items():
                        if pos in k_pos._before:
                            k_pos._before[pos] += occurence
                        else:
                            k_pos._before[pos] = occurence
                    # And after
                    for pos, occurence in val._after.items():
                        if pos in k_pos._after:
                            k_pos._after[pos] += occurence
                        else:
                            k_pos._after[pos] = occurence
            else:
                self._parts_of_speech[raw] = val

    def teach_words(self, words):
        """
        Process given words to adjust knowledge probabilities.
        """

        for raw, word in words.items():
            if raw in self._words:
                k_word = self._words[raw]
                k_word.occurence += word.occurence
                for pos, pos_occurence in word._being.items():
                    if pos in k_word._being:
                        k_word._being[pos] += pos_occurence
                    else:
                        k_word._being[pos] = pos_occurence
            else:
                self._words[raw] = word

    def teach(self, words = {}, parts_of_speech = {}):
        """
        Teach this context with given words and/or parts_of_speech.
        This is the main method to train the context.
        """

        self.teach_words(words)
        self.teach_parts_of_speech(parts_of_speech)

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
        
        # Check if we passed a parent chain
        if type(pos_obj) is dict:
            # Retrieve the sum for children
            leaves = pos._get_leaves(pos_obj)
            computed = 0.0
            for leaf in leaves:
                computed += self._being.get(leaf, 0.0)
            return computed / self.occurence

        if pos_obj not in self._being:
            return 0.0
        
        return self._being[pos_obj] / self.occurence

    def __repr__(self):
        return "<%s>" % self.occurence