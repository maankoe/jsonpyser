from typing import Dict, Type, List
import io

from genson.context_decoding import ContextHandler
from genson.array_decoding import ArrayContextHandler
from genson.string_decoding import StringContextHandler
from genson.decoding_utils import *


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
