from typing import Any, Dict, Type
from abc import ABC, abstractmethod
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


class ContextHandler:
    start_char: str
    end_char: str
    input: Any
    output: Any

    def __init__(self, enter_char):
        self.enter_char = enter_char

    @abstractmethod
    def is_end_char(self, x):
        pass

    @abstractmethod
    def accept_char(self, x):
        pass

    @abstractmethod
    def accept_output(self, x):
        pass

    @abstractmethod
    def get_output(self):
        pass

    def __repr__(self):
        return f"<{self.start_char}:{self.input}->{self.output}>"


class ArrayContextHandler(ContextHandler):
    def __init__(self, enter_char):
        super().__init__(enter_char)
        self.start_char = "["
        self.end_char = "]"
        self.input = []
        self.output = []
        self.is_closed = False

    def is_end_char(self, x):
        return x == self.end_char

    def _parse_item(self):
        input_str = "".join(self.input).strip()
        if len(input_str) > 0:
            self.output.append(decode_item(input_str))
        self.input = []

    def accept_char(self, x):
        if self.is_closed:
            raise ValueError("Extra characters outside context")
        if x == self.end_char:
            self._parse_item()
            self.is_closed = True
        elif x == ",":
            self._parse_item()
        else:
            self.input.append(x)

    def accept_output(self, output):
        self.output.append(output)

    def get_output(self):
        if not self.is_closed:
            raise ValueError("Unclosed bracket")
        return self.output



context_handlers: Dict[str, Type[ContextHandler]] = {
    "[": ArrayContextHandler,
    # ",": {"end_char": ",", "handler": ItemHandler}
}

def is_whitespace(x):
    return x in [" "]

class JSONStreamDecoder():
    def __init__(self):
        self.context_stack = []

    @property
    def current_context(self):
        return self.context_stack[-1]

    def enter_context(self, start_char):
        handler = context_handlers[start_char]
        self.context_stack.append(handler(start_char))

    def exit_context(self, end_char):
        self.current_context.accept_char(end_char)
        if len(self.context_stack) > 1:
            closed_context = self.context_stack.pop()
            self.current_context.accept_output(closed_context.get_output())

    def process_char(self, x):
        if is_whitespace(x):
            pass
        elif len(self.context_stack) > 0 and self.current_context.is_end_char(x):
            self.exit_context(x)
        elif x in context_handlers:
            self.enter_context(x)
        else:
            self.current_context.accept_char(x)

    def decode(self, stream):
        x = stream.read(1)
        while x:
            self.process_char(x)
            print(x, self.context_stack)
            x = stream.read(1)
        return self.context_stack.pop().get_output()


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
