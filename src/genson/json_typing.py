from typing import Dict, Iterable


def is_dict(x):
    return isinstance(x, Dict)

def is_array(x):
    return isinstance(x, Iterable) and not is_dict(x) and not is_str(x)

def is_object(x):
    return not is_dict(x) and not is_array(x)

def is_str(x):
    return isinstance(x, str)

def is_number(x):
    return isinstance(x, int) or isinstance(x, float)