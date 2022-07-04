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


def decode_json_string(json_string: str):
    json_string = json_string.lstrip()
    if len(json_string) == 0:
        return None
    elif json_string[0] != "[":
        return decode_item(json_string.strip())
    elif json_string[0] == "[":
        return JSONDecoder().decode(json_string)



# class JSONContext:
#     def __init__(self):
#         self.output = output
#         self.context = []


# class JSONStreamDecoder():
#     def __init__(self):
#         self.context = []
#         self.output = None
#         self.context_stack = []
#         self.json_stack = []
#
#     def decode_context(self, end_context_char):
#         context_json = item_json(self.context)
#         # if end_context_char == "," and len(context_json) == 0:
#         #     raise ValueError("adsf")
#         if len(context_json) > 0:
#             self.output.append(decode_item(context_json))
#             self.context = []
#
#     def decode_array(self, stream):
#         decoder = JSONStreamDecoder()
#         data = decoder.decode(stream, "[")
#         self.output.append(data)
#
#     def initialize_output(self, start_char):
#         if start_char == "[":
#             self.output = []
#         self.enter_context("[")
#
#     def enter_context(self, open_context_char):
#         self.context_stack.append(open_context_char)
#
#     def exit_context(self, close_context_char):
#         open_context_char = self.context_stack.pop()
#         print(open_context_char, close_context_char)
#         if open_context_char == "[" and close_context_char != "]":
#             raise ValueError("Mismatching bracket")
#
#     def decode(self, stream, context_char):
#         self.initialize_output(context_char)
#         x = stream.read(1)
#         while x:
#             if x == ",":
#                 self.decode_context(x)
#             elif x == "[":
#                 self.decode_array(stream)
#             elif x == "]":
#                 self.decode_context(x)
#                 self.exit_context(x)
#                 break
#             elif x == "}":
#                 self.exit_context(x)
#                 break
#             else:
#                 self.context.append(x)
#             x = stream.read(1)
#         print(self.context_stack, self.context, self.output)
#         if len(self.context_stack) > 0:
#             raise ValueError("Unclosed bracket")
#         return self.output

class JSONContext:
    def __init__(self, start_char, end_char):
        self.input = []
        self.start_char = start_char
        self.end_char = end_char
        self.initialize_output(start_char)

    def initialize_output(self, start_char):
        if start_char == "[":
            self.output = []
            self.is_closed = False
        else:
            self.is_closed = True
            self.output = None

    def parse_input(self):
        input_str = "".join(self.input).strip()
        if len(input_str) > 0:
            self.output.append(decode_item(input_str))
        self.input = []

    def next_char(self, char):
        if self.is_closed:
            raise ValueError("Extra characters outside context")
        if char == self.end_char:
            self.parse_input()
            self.is_closed = True
        elif char == ",":
            self.parse_input()
        else:
            self.input.append(char)

    def add_output(self, output):
        if self.start_char == "[":
            self.output.append(output)
        else:
            self.output = output

    def get_output(self):
        if not self.is_closed:
            raise ValueError("Unclosed bracket")
        return self.output

    def __repr__(self):
        return f"<{self.start_char}:{self.input}->{self.output}>"


class JSONStreamDecoder():
    def __init__(self):
        self.decoder_stack = []

    def decode(self, stream):
        x = stream.read(1)
        while x:
            if x == " ":
                pass
            elif x == ",":
                self.decoder_stack[-1].next_char(x)
            elif x == "[":
                self.decoder_stack.append(JSONContext(x, "]"))
            elif x == "]":
                self.decoder_stack[-1].next_char(x)
                if len(self.decoder_stack) > 1:
                    closed_context = self.decoder_stack.pop()
                    self.decoder_stack[-1].add_output(closed_context.get_output())
            else:
                self.decoder_stack[-1].next_char(x)
            print(x, self.decoder_stack)
            x = stream.read(1)
        return self.decoder_stack.pop().get_output()


def decode_json(json_string: str):
    json_string = json_string.lstrip()
    if len(json_string) == 0:
        return None
    elif json_string[0] != "[":
        return decode_item(json_string.strip())
    elif json_string[0] == "[":
        import io
        stream = io.StringIO(json_string)
        # stream.seek(1)
        # return JSONStreamDecoder().decode(stream, "[")
        return JSONStreamDecoder().decode(stream)
