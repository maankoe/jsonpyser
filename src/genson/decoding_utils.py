from typing import AnyStr
import io
import re


int_re = re.compile("^[0-9]+$")
float_re = re.compile("^[0-9]*[.]?[0-9]*$")


def is_escape(x: AnyStr):
    return len(x) == 1 and x == "\\"


def is_whitespace(x: AnyStr):
    return all(_ in "\t " for _ in x)


def read_to_non_whitespace(stream: io.StringIO):
    x = stream.read(1)
    while is_whitespace(x):
        x = stream.read(1)
    return x


def is_int_match(x: AnyStr):
    return int_re.fullmatch(x) is not None


def is_float_match(x: AnyStr):
    return float_re.fullmatch(x) is not None


def decode_int(x: AnyStr):
    return int(x)


def decode_float(x: AnyStr):
    return float(x)


def decode_item(x: AnyStr):
    if len(x) == 0:
        return None
    elif is_int_match(x):
        return decode_int(x)
    elif is_float_match(x):
        return decode_float(x)
    else:
        raise ValueError("Unrecognised item")
