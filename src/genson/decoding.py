from typing import Any, Dict, Type, List
from abc import ABC, abstractmethod
import re
import io

int_re = re.compile("^[0-9]+$")
float_re = re.compile("^[0-9]+[.][0-9]*$")

def is_whitespace(x):
    return x in [" "]

def is_escape(x):
    return x == "\\"

def read_to_non_whitespace(stream):
    x = stream.read(1)
    while is_whitespace(x):
        x = stream.read(1)
    return x

def is_int_match(x):
    return int_re.fullmatch(x)

def is_float_match(x):
    return float_re.fullmatch(x)

def is_string_match(x):
    return x.startswith('"') and x.endswith('"')

def decode_int(number_json):
    return int(number_json)

def decode_float(number_json):
    return float(number_json)

def decode_string(string_json):
    return string_json

def decode_item(item_json):
    if len(item_json) == 0:
        return None
    elif is_int_match(item_json):
        return decode_int(item_json)
    elif is_float_match(item_json):
        return decode_float(item_json)
    elif is_string_match(item_json):
        return decode_string(item_json)
    else:
        raise ValueError("Unrecognised item")

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
    enter_char: str
    output: Any = None

    def __init__(self, enter_char):
        self.enter_char = enter_char
        self.is_closed = False
        self.input = []

    @abstractmethod
    def accepts_children(self):
        pass

    @abstractmethod
    def is_end_char(self, x):
        pass

    @abstractmethod
    def accept_char(self, x):
        pass

    @abstractmethod
    def accept_item(self, x):
        pass

    @abstractmethod
    def get_output(self):
        pass

    def has_input(self):
        return len(self.input) > 0

    def __repr__(self):
        return f"<{self.enter_char}:{self.input}->{self.output}>"


class IterableContextHandler(ContextHandler):
    def __init__(self, enter_char, start_char, end_chars, item_separators):
        super().__init__(enter_char)
        self.start_char = start_char
        self.end_chars = end_chars
        self.item_separators = item_separators
        self._just_accepted_output = False

    @abstractmethod
    def _parse_input_as_item(self):
        pass

    def accepts_children(self):
        return True

    def is_end_char(self, x):
        return x in self.end_chars

    def is_item_separator(self, x):
        return x in self.item_separators

    def is_input_char_valid(self, x):
        if self.is_item_separator(x) and not self.is_item_separator_expected():
            raise ValueError(f"Empty item")
        return not is_whitespace(x)

    def accept_char(self, x):
        if self.is_input_char_valid(x):
            self.is_closed = self.is_closed or self.is_end_char(x)
            if self.is_item_separator(x) or self.is_closed:
                self._parse_input_as_item()
            else:
                self.input.append(x)
            self._just_accepted_output = False

    def is_item_separator_expected(self):
        return self.has_input() or self._just_accepted_output

    def accept_item(self, output):
        self.output.append(output)
        self._just_accepted_output = True

    def get_output(self):
        return self.output


class ArrayContextHandler(IterableContextHandler):
    def __init__(self, enter_char):
        super().__init__(enter_char, "[", "]", ",")
        self.output = []

    def _parse_input_as_item(self):
        if self.has_input():
            self.output.append(decode_item("".join(self.input)))
        self.input = []


class StringContextHandler(ContextHandler):
    def __init__(self, enter_char, end_chars=None):
        super().__init__(enter_char)
        if end_chars is None:
            self.end_chars = "\""
        else:
            self.end_chars = end_chars

    def accepts_children(self):
        return False

    def escaped(self):
        return len(self.input) > 0 and is_escape(self.input[-1])

    def is_end_char(self, x):
        return x in self.end_chars and not self.escaped()

    def accept_char(self, x):
        self.is_closed = self.is_closed or self.is_end_char(x)
        if self.escaped() and not is_escape(x):
            self.input.pop()
        self.input.append(x)

    def accept_item(self, x):
        raise Exception("String context cannot accept child items")

    def get_output(self):
        return decode_string("".join(self.input[:-1]))


class RootContext(ContextHandler):
    def __init__(self):
        super().__init__("")
        self.output = None
        self.is_closed = False

    def accepts_children(self):
        return not self.is_closed

    def is_end_char(self, x):
        return False

    def accept_char(self, x):
        pass

    def accept_item(self, x):
        self.is_closed = True
        self.output = x

    def get_output(self):
        return self.output


class JSONStreamDecoder():
    def __init__(self, context_handlers):
        self.context_stack: List[ContextHandler] = [RootContext()]
        self.context_handlers = context_handlers

    @property
    def current_context(self):
        return self.context_stack[-1]

    def is_new_context(self, x):
        return self.current_context.accepts_children() and x in self.context_handlers

    def enter_context(self, start_char):
        handler = context_handlers[start_char]
        self.context_stack.append(handler(start_char))

    def is_current_context_root(self):
        return isinstance(self.current_context, RootContext)

    def exit_context(self):
        if not self.is_current_context_root():
            output = self.get_current_context_output()
            self.context_stack.pop()
            self.current_context.accept_item(output)
        # elif len(self.context_stack) == 0:
        #     raise Exception("No context from which to exit.")

    def add_char_to_current_context(self, x):
        if self.current_context.is_closed and not is_whitespace(x):
            raise ValueError("Extra characters after close")
        self.current_context.accept_char(x)

    def get_current_context_output(self):
        if not self.current_context.is_closed:
            raise ValueError("Exiting from unclosed context")
        return self.current_context.get_output()

    def process_char(self, x):
        if self.current_context.is_end_char(x):
            self.add_char_to_current_context(x)
            self.exit_context()
        elif self.is_new_context(x):
            self.enter_context(x)
        else:
            self.add_char_to_current_context(x)

    def decode(self, stream):
        x = read_to_non_whitespace(stream)
        if not self.is_new_context(x):
            input_str = x + stream.read()
            return decode_item(input_str.strip())
        while x:
            self.process_char(x)
            print(x, self.context_stack)
            x = stream.read(1)
        return self.get_current_context_output()


context_handlers: Dict[str, Type[ContextHandler]] = {
    "[": ArrayContextHandler,
    '"': lambda x: StringContextHandler(x, end_chars="\""),
}


def decode_json(json_string: str):
    return JSONStreamDecoder(context_handlers).decode(io.StringIO(json_string))
