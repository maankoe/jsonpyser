from genson.json_typing import *

_string_open = '"'
_string_close = '"'
_array_open = "["
_array_close = "]"
_map_open = "{"
_map_close = "}"
_class_open = "<"
_class_close = ">"
_item_sep = ", "
_key_value_sep = ": "
_null = "null"

def dump_string(string):
    return _string_open + string + _string_close

def dump_number(number):
    return repr(number)

def dump_class(object):
    return _class_open + repr(object) + _class_close

def dump_object(object):
    if is_str(object):
        return dump_string(object)
    elif is_number(object):
        return dump_number(object)
    else:
        return dump_class(object)

def dump_array(array):
    inner_str = _item_sep.join(dump_jsonable(x) for x in array)
    return _array_open + inner_str + _array_close

def dump_key_value_pair(key, value):
    return f"{dump_string(key)}{_key_value_sep}{dump_jsonable(value)}"

def dump_dictionary(map):
    inner_str = _item_sep.join(dump_key_value_pair(k, v) for k, v in map.items())
    return _map_open + inner_str + _map_close

def dump_null():
    return _null

def dump_jsonable(jsonable) -> str:
    if is_object(jsonable):
        return dump_object(jsonable)
    elif is_array(jsonable):
        return dump_array(jsonable)
    elif is_map(jsonable):
        return dump_dictionary(jsonable)
    elif is_null(jsonable):
        return dump_null()
