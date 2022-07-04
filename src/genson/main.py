from typing import Dict, Iterable, AnyStr

from genson.json_typing import *

def dump_object(jsonable_object):
    if is_str(jsonable_object):
        return '"' + jsonable_object + '"'
    elif is_number(jsonable_object):
        return repr(jsonable_object)

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
