import knowledge

class PartOfSpeech:
    """
    Represents a part of speech (ie. a  linguistic category).
    """
    
    def __init__(self, value, parent_value=None, occurence=1):
        self.value = value
        self.occurence = occurence
        self.parent = parent_value
        self.before = {}
        self.after = {}
    
    def being_before(self, pos_obj):
        """
        Gets the probability of having this pos before given pos_obj.
        """
        
        if pos_obj not in self.after:
            return 0.0
        
        return self.after[pos_obj] / self.occurence
    
    def being_after(self, pos_obj):
        """
        Gets the probability of having this pos after given pos_obj.
        """
    
        if pos_obj not in self.before:
            return 0.0
        
        return self.before[pos_obj] / self.occurence
        
    def __str__(self):
        return "%s - %s" % (self.value, self.occurence)
    
    def __repr__(self):
        return "%s" % self.occurence
    
    @staticmethod
    def create_from_tokens(tokens, child_separator=':', start_sentence_value='None', end_sentence_value='Punc'):
        """
        Create PartOfSpeech objects as needed based on given tokens
        and ties together each PartOfSpeech.
        """
        
        value_to_pos = {}
        value_to_pos[start_sentence_value] = PartOfSpeech(start_sentence_value)
        
        # Let's build our PartOfSpeech objects and increment occurence each time we find the same pos
        # TODO Should we increment the start sentence pos occurence?
        for token in tokens:
            tname = token[1]
            # Look for nested pos (1 depth MAX)
            tname_splitted = tname.split(child_separator)
            if len(tname_splitted) == 2:
                tname, tname_child = tname_splitted
                if tname not in value_to_pos:                    
                    value_to_pos[tname] = { tname_child: PartOfSpeech(tname_child, tname) }
                else:
                    # The parent exists, look for the child
                    if tname_child not in value_to_pos[tname]:
                        value_to_pos[tname][tname_child] = PartOfSpeech(tname_child, tname)
                    else:
                        value_to_pos[tname][tname_child].occurence += 1
            else:
                if tname not in value_to_pos:
                    value_to_pos[tname] = PartOfSpeech(tname)
                else:
                    value_to_pos[tname].occurence += 1

        # For now, let's loop twice on tokens
        
        # Sentence start
        previous_tag = start_sentence_value
        p_pos = value_to_pos[previous_tag]
        value_to_word = {}
        
        for token in tokens:
            word, tag = token
            word = word.lower()
            tag_splitted = tag.split(child_separator)
            
            # Check if nested pos
            if len(tag_splitted) == 2:
                c_pos = value_to_pos[tag_splitted[0]][tag_splitted[1]]
            else:
                c_pos = value_to_pos[tag]
            
            # Check if word exists
            if word not in value_to_word:
                value_to_word[word] = knowledge.Word(word)
            else:
                value_to_word[word].occurence += 1
            
            c_word = value_to_word[word]
            
            # Now check occurence for the c_pos
            if c_pos not in c_word.being:
                c_word.being[c_pos] = 1
            else:
                c_word.being[c_pos] += 1
            
            # Previous -> Current
            if c_pos not in p_pos.after:
                p_pos.after[c_pos] = 1
            else:
                p_pos.after[c_pos] += 1
                
            # Current -> Previous
            if p_pos not in c_pos.before:
                c_pos.before[p_pos] = 1
            else:
                c_pos.before[p_pos] += 1
            
            if c_pos.value == end_sentence_value:
                previous_tag = start_sentence_value
                p_pos = value_to_pos[previous_tag]
            else:
                previous_tag = tag
                p_pos = c_pos
        
        ################# EXPERIMENTS
        
        a = value_to_pos['Det']['Pos']
        b = value_to_pos['Nom']
        w = value_to_word['son']
        
        print(a.being_before(b))
        print(b.being_after(a))
        print(w.being_a(b))
        
#         xxx = [value_to_pos['Nom'].after[x] for x in value_to_pos['Nom'].after if x.parent and x.parent == 'Ver']
#         print(sum(xxx))
#         
#         print('after:')
#         
#         for a, b in value_to_pos['Nom'].after.items():
#             print(a.value, a.parent, b)
#             
#         print('before:')
#         
#         for a, b in value_to_pos['Ver']['Impe'].before.items():
#             print(a.value, a.parent, b)
        
#         for a, b in value_to_pos['Ver']['Pres'].before.items():
#             print(a.value, a.parent, b)
        
        ################# /EXPERIMENTS
        
        return value_to_pos