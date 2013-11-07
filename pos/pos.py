class PartOfSpeech:
    """
    Represents a part of speech (ie. a  linguistic category).
    """
    
    def __init__(self, value, occurence=1):
        self.value = value
        self.occurence = occurence
    
    def __str__(self):
        return "%s - %s" % (self.value, self.occurence)
    
    def __repr__(self):
        return "%s" % self.occurence
    
    @staticmethod
    def create_from_tokens(tokens, child_separator=':'):
        """
        Create PartOfSpeech objects as needed based on given tokens.
        It computes emission and transition probabilities and
        ties together each PartOfSpeech.
        """
        
        value_to_pos = {}
        
        # Let's build our PartOfSpeech objects and increment occurence each time we find the same pos
        for token in tokens:
            tname = token[1]
            # Look for nested pos (1 depth MAX)
            tname_splitted = tname.split(child_separator)
            if len(tname_splitted) == 2:
                tname, tname_child = tname_splitted
                if tname not in value_to_pos:                    
                    value_to_pos[tname] = { tname_child: PartOfSpeech(tname_child) }
                else:
                    # The parent exists, look for the child
                    if tname_child not in value_to_pos[tname]:
                        value_to_pos[tname][tname_child] = PartOfSpeech(tname_child)
                    else:
                        value_to_pos[tname][tname_child].occurence += 1
            else:
                if tname not in value_to_pos:
                    value_to_pos[tname] = PartOfSpeech(tname)
                else:
                    value_to_pos[tname].occurence += 1
        
        # TODO Build bigrams
        
        return value_to_pos