import pos

def find_child(tag, value_to_pos, parent_value = None, child_separator = ':'):
    """
    Find or create a nested PartOfSpeech and returns it.
    """

    chain = tag.split(child_separator, 1)
    parent = chain[0]
    if len(chain) > 1:
        parent_val = value_to_pos.setdefault(parent, {})
        return find_child(chain[1], parent_val, parent, child_separator)
    else:
        child = value_to_pos.setdefault(parent, pos.PartOfSpeech(parent, parent_value, 0))
        value_to_pos[parent] = child
        return child

def get_leaves(look_in):
    """
    Find leaves in dictionary.
    """

    res = []

    for key, val in look_in.items():
        if type(val) is dict:
            res.extend(get_leaves(val))
        else:
            res.append(val)

    return res