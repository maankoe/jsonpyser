from typing import Dict, Iterable, AnyStr

from genson.json_typing import *

def dump_string(string):
    return '"' + string + '"'

def dump_number(number):
    return repr(number)

def dump_object(object):
    if is_str(object):
        return dump_string(object)
    elif is_number(object):
        return repr(object)

def dump_array(array):
    inner_str = ', '.join(dump_jsonable(x) for x in array)
    return "[" + inner_str + "]"

def dump_key_value_pair(key, value):
    return f"{dump_string(key)}: {dump_jsonable(value)}"

def dump_dictionary(map):
    inner_str = ', '.join(dump_key_value_pair(k, v) for k, v in map.items())
    return "{" + inner_str + "}"

def dump_jsonable(jsonable) -> str:
    if is_object(jsonable):
        return dump_object(jsonable)
    elif is_array(jsonable):
        return dump_array(jsonable)
    elif is_map(jsonable):
        return dump_dictionary(jsonable)
