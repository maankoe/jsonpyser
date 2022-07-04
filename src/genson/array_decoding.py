from genson.context_decoding import IterableContextHandler
from genson.decoding_utils import decode_item

class ArrayContextHandler(IterableContextHandler):
    def __init__(self, enter_char):
        super().__init__(enter_char, "[", "]", ",")
        self.output = []

    def _parse_input_as_item(self):
        if self.has_input():
            self.output.append(decode_item("".join(self.input)))
        self.input = []