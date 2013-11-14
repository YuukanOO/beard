import knowledge

def create_from_tokens(tokens, child_separator=':', start_sentence_value='None', end_sentence_value='Punc'):
    """
    Create PartOfSpeech objects as needed based on given tokens
    and ties together each PartOfSpeech.
    """
    
    value_to_pos = {}
    value_to_word = {}
    
    value_to_pos[start_sentence_value] = PartOfSpeech(start_sentence_value)
    
    p_tag = start_sentence_value # Previous pos tag value
    p_pos = value_to_pos[p_tag] # Previous pos object
    c_pos = None # Current pos object
    c_word = None # Current word object
    
    # Let's build our PartOfSpeech objects and increment occurence each time we find the same pos
    # TODO Should we increment the start sentence pos occurence?
    for token in tokens:
        word, tag_name = token
        word = word.lower()
        # Look for nested pos (1 depth MAX at the moment)
        tag_name_splitted = tag_name.split(child_separator)
        if len(tag_name_splitted) >= 2:
            tag_name, tag_name_child = tag_name_splitted
            # Look if this pos already exists
            if tag_name not in value_to_pos:
                c_pos = PartOfSpeech(tag_name_child, tag_name)
                value_to_pos[tag_name] = { tag_name_child: c_pos }
            else:
                # Parent exists, look for the child
                if tag_name_child not in value_to_pos[tag_name]:
                    c_pos = PartOfSpeech(tag_name_child, tag_name)
                    value_to_pos[tag_name][tag_name_child] = c_pos
                else:
                    c_pos = value_to_pos[tag_name][tag_name_child]
                    c_pos.occurence += 1
        else:
            if tag_name not in value_to_pos:
                c_pos = PartOfSpeech(tag_name)
                value_to_pos[tag_name] = c_pos
            else:
                c_pos = value_to_pos[tag_name]
                c_pos.occurence += 1
        
        # Check if c_pos is defined (It should be btw)
        if c_pos:
            # Check if word exists
            if word not in value_to_word:
                c_word = knowledge.Word(word)
                value_to_word[word] = c_word
            else:
                c_word = value_to_word[word]
                c_word.occurence += 1
            
            # Now check occurence for the c_pos in the c_word
            if c_pos not in c_word._being:
                c_word._being[c_pos] = 1
            else:
                c_word._being[c_pos] += 1
                
            # Previous -> Current
            if c_pos not in p_pos._after:
                p_pos._after[c_pos] = 1
            else:
                p_pos._after[c_pos] += 1
                
            # Current -> Previous
            if p_pos not in c_pos._before:
                c_pos._before[p_pos] = 1
            else:
                c_pos._before[p_pos] += 1
                
            if c_pos.value == end_sentence_value:
                p_tag = start_sentence_value
                p_pos = value_to_pos[p_tag]
            else:
                p_tag = c_pos.value
                p_pos = c_pos
        else:
            raise
    
    ################# EXPERIMENTS
        
#         xxx = [value_to_pos['Nom']._after[x] for x in value_to_pos['Nom']._after if x.parent and x.parent == 'Ver']
#         print(sum(xxx))
#         
#         print('_after:')
#         
#         for a, b in value_to_pos['Nom']._after.items():
#             print(a.value, a.parent, b)
#             
#         print('_before:')
#         
#         for a, b in value_to_pos['Ver']['Impe']._before.items():
#             print(a.value, a.parent, b)
    
#         for a, b in value_to_pos['Ver']['Pres']._before.items():
#             print(a.value, a.parent, b)
    
    ################# /EXPERIMENTS
    
    return { 'words' : value_to_word, 'poss' : value_to_pos }

class PartOfSpeech:
    """
    Represents a part of speech (ie. a  linguistic category).
    """
    
    def __init__(self, value, parent_value=None, occurence=1):
        self.value = value
        self.occurence = occurence
        self.parent = parent_value
        self._before = {}
        self._after = {}
    
    def being_before(self, pos_obj):
        """
        Gets the probability of having this pos _before given pos_obj.
        """
        
        if pos_obj not in self._after:
            return 0.0
        
        return self._after[pos_obj] / self.occurence
    
    def being_after(self, pos_obj):
        """
        Gets the probability of having this pos _after given pos_obj.
        """
    
        if pos_obj not in self._before:
            return 0.0
        
        return self._before[pos_obj] / self.occurence
        
    def __str__(self):
        return "%s - %s" % (self.value, self.occurence)
    
    def __repr__(self):
        return "%s" % self.occurence