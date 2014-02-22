import codecs, re, knowledge

def _find_child(tag, value_to_pos, parent_value = None, child_separator = ':'):
    """
    Find a nested PartOfSpeech.
    """

    chain = tag.split(child_separator, 1)
    parent = chain[0]
    if len(chain) > 1:
        parent_val = value_to_pos.setdefault(parent, {})
        return _find_child(chain[1], parent_val, parent, child_separator)
    else:
        child = value_to_pos.setdefault(parent, PartOfSpeech(parent, parent_value, 0))
        value_to_pos[parent] = child
        return child

def _get_leaves(look_in):
    """
    Find leaves in dictionary.
    """

    res = []

    for key, val in look_in.items():
        if type(val) is dict:
            res.extend(_get_leaves(val))
        else:
            res.append(val)

    return res

def create_from_tokens(tokens, child_separator = ':', start_sentence_value = 'None', end_sentence_value = 'Punc'):
    """
    Create PartOfSpeech objects as needed based on given tokens
    and ties together each PartOfSpeech.
    """

    value_to_pos = {} # Dictionary to link raw_tag to PartOfSpeech object
    value_to_word = {} # Dictionary to link raw_word to Word object

    # Start by creating our start sentence pos
    start_pos = value_to_pos.setdefault(start_sentence_value, PartOfSpeech(start_sentence_value))
    prev_pos = start_pos
    cur_word = None
    cur_pos = None

    for token in tokens:
        raw_word, raw_tag = token
        raw_word = raw_word.lower() # To avoid mistakes, let's lower it

        # Retrieve the Word object
        cur_word = value_to_word.setdefault(raw_word, knowledge.Word(cur_word, occurence = 0))
        # Increment occurence
        cur_word.occurence += 1

        # Retrieve the PartOfSpeech object
        cur_pos = _find_child(raw_tag, value_to_pos) #value_to_pos.setdefault(raw_tag, PartOfSpeech(raw_tag, occurence = 0))
        # Increment occurence
        cur_pos.occurence += 1

        # Increment the change for this word to be of type pos
        cur_word._being.setdefault(cur_pos, 0)
        cur_word._being[cur_pos] += 1

        # Inform the previous part of speech that it appears before the current one
        prev_pos._after.setdefault(cur_pos, 0)
        prev_pos._after[cur_pos] += 1

        # Inform the current part of speech that it appears after the previous one
        cur_pos._before.setdefault(prev_pos, 0)
        cur_pos._before[prev_pos] += 1

        # Let's update the chain
        if raw_tag == end_sentence_value:
            prev_pos = start_pos
        else:
            prev_pos = cur_pos

    return { 'words' : value_to_word, 'parts_of_speech' : value_to_pos }

class Tokenizer:

    def __init__(self, delimiter = '/'):
        self.delimiter = delimiter

    def tokenize_from_file(self, filepath, encoding = 'utf-8'):
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

class PartOfSpeech:
    """
    Represents a part of speech (ie. a  linguistic category).
    """

    def __init__(self, value, parent_value = None, occurence = 1):
        self.value = value
        self.occurence = occurence
        self.parent = parent_value
        self._before = {}
        self._after = {}

    def _being(self, look_in, pos_obj):
        """
        Internal method to check if given pos_obj is contained in
        look_in array and computes probability.
        """

        # Check if we passed a parent chain
        if type(pos_obj) is dict:
            # Retrieve the sum for children
            leaves = _get_leaves(pos_obj)
            computed = 0.0
            for leaf in leaves:
                computed += look_in[leaf]
            computed /= len(leaves)
            return computed / self.occurence

        if pos_obj not in look_in:
            return 0.0

        return look_in[pos_obj] / self.occurence

    def being_before(self, pos_obj):
        """
        Gets the probability of having this pos _before given pos_obj.
        """

        return self._being(self._after, pos_obj)

    def being_after(self, pos_obj):
        """
        Gets the probability of having this pos _after given pos_obj.
        """

        return self._being(self._before, pos_obj)

    def __repr__(self):
        return "<%s (%s)>" % (self.value, self.occurence)

class Tagger:

    def tag(self, string, context):
        """
        Tag the given string using the given context.
        """