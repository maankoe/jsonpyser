from typing import Dict, Iterable, AnyStr

from genson.json_typing import *

def dump_str(string):
    return '"' + string + '"'

def dump_number(number):
    return repr(number)

def dump_object(object):
    if is_str(object):
        return dump_str(object)
    elif is_number(object):
        return repr(object)

# def dump_array(jsonable_array):
#     inner_str = ', '.join(jsonable_array)
#     return f'[{inner_str}]'

def dumps(jsonable) -> str:
    if is_object(jsonable):
        return dump_object(jsonable)
    elif is_array(jsonable):
        return "[]"
    elif is_dict(jsonable):
        return "{}"
