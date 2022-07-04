import re


int_re = re.compile("^[0-9]+$")
float_re = re.compile("^[0-9]+[.][0-9]*$")


def is_int_match(x):
    return int_re.match(x)

def is_float_match(x):
    return float_re.match(x)

def decode_int(number):
    return int(number)

def decode_float(number):
    return float(number)

def decode_string(string):
    return string[1:-1]

# def array_end_index(array):
#     return array.index("]")

def decode_array(array):
    inner = decode_json(array[1:-1])
    if inner is not None:
        return [inner]
    else:
        return []

def decode_json(json_string):
    if len(json_string) == 0:
        return None
    elif json_string[0] == "[":
        return decode_array(json_string)
    elif is_int_match(json_string):
        return decode_int(json_string)
    elif is_float_match(json_string):
        return decode_float(json_string)
    else:
        return decode_string(json_string)