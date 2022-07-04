from genson.context_decoding import ContextHandler
from genson.decoding_utils import is_escape


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
        return "".join(self.input[:-1])