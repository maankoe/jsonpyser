import re


int_re = re.compile("^[0-9]+$")
float_re = re.compile("^[0-9]+[.][0-9]*$")


def is_escape(x):
    return x == "\\"


def is_whitespace(x):
    return x in [" "]


def read_to_non_whitespace(stream):
    x = stream.read(1)
    while is_whitespace(x):
        x = stream.read(1)
    return x


def is_int_match(x):
    return int_re.fullmatch(x)


def is_float_match(x):
    return float_re.fullmatch(x)


def decode_int(number_json):
    return int(number_json)


def decode_float(number_json):
    return float(number_json)


def decode_item(item_json):
    if len(item_json) == 0:
        return None
    elif is_int_match(item_json):
        return decode_int(item_json)
    elif is_float_match(item_json):
        return decode_float(item_json)
    else:
        raise ValueError("Unrecognised item")
