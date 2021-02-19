import numpy as np
from collections import defaultdict 


def get_text(text, list_name):
    text = text[1:]
    sub_text = []
    i = 0
    while text[i] not in list_name:
        sub_text.append(text[i])
        i += 1
        if i >= len(text):
            break

    return sub_text


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def seq_in_seq(subseq, seq):
    while subseq[0] in seq:
        index = seq.index(subseq[0])
        if subseq == seq[index:index + len(subseq)]:
            return index
        else:
            seq = seq[index + 1:]
    else:
        return False
    
    
def fill_dict_for_df(dic_to_fill, keys_names, values, title) :
    
    if isinstance(values[0], list) :
        for i in range(len(values[0])) :
            dic_to_fill['Title'].append(title)
    else :
        dic_to_fill['Title'].append(title)
    
    for i, name in enumerate(keys_names) :
        value_s = values[i]
        if isinstance(value_s, list) :
            for value in value_s :
                dic_to_fill[name].append(value)
        else :
            dic_to_fill[name].append(value_s)
            
    return dic_to_fill