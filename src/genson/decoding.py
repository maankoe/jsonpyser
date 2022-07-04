import re


int_re = re.compile("^[0-9]+$")
float_re = re.compile("^[0-9]+[.][0-9]*$")


def is_int_match(x):
    return int_re.match(x)

def is_float_match(x):
    return float_re.match(x)

def decode_int(number_json):
    return int(number_json)

def decode_float(number_json):
    return float(number_json)

def decode_string(string_json):
    return string_json[1:-1]


def decode_item(item_json):
    if len(item_json) == 0:
        return None
    elif is_int_match(item_json):
        return decode_int(item_json)
    elif is_float_match(item_json):
        return decode_float(item_json)
    else:
        return decode_string(item_json)

def item_json(context):
    item_json = "".join(context)
    return item_json.strip()


class JSONDecoder():
    def __init__(self):
        self.context = []
        self.output = None
        self.pos = 0

    def decode_context(self):
        context_json = item_json(self.context)
        if len(context_json) > 0:
            self.output.append(decode_item(context_json))
            self.context = []

    def decode_array(self, json_string):
        decoder = JSONDecoder()
        data = decoder.decode(json_string)
        self.pos += decoder.pos + 1
        self.output.append(data)

    def initialize_output(self, start_char):
        if start_char == "[":
            self.output = []
        self.pos += 1

    def decode(self, json_string):
        self.initialize_output(json_string[0])
        while self.pos < len(json_string):
            x = json_string[self.pos]
            if x == ",":
                self.decode_context()
            elif x == "[":
                self.decode_array(json_string[self.pos:])
            elif x == "]":
                self.decode_context()
                break
            else:
                self.context.append(x)
            self.pos += 1
        return self.output

def decode_json(json_string: str):
    json_string = json_string.lstrip()
    if len(json_string) == 0:
        return None
    elif json_string[0] != "[":
        return decode_item(json_string.strip())
    elif json_string[0] == "[":
        return JSONDecoder().decode(json_string)
