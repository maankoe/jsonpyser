from typing import Dict, Iterable


def is_map(x):
    return isinstance(x, Dict)

def is_array(x):
    return isinstance(x, Iterable) and not is_map(x) and not is_str(x)

def is_object(x):
    return not is_map(x) and not is_array(x) and not is_null(x)

def is_str(x):
    return isinstance(x, str)

def is_number(x):
    return isinstance(x, int) or isinstance(x, float)

def is_null(x):
    return x is None