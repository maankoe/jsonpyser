from typing import Any
from abc import ABC, abstractmethod

from genson.decoding_utils import is_whitespace


class ContextHandler(ABC):
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

    def _is_item_separator(self, x):
        return x in self.item_separators

    def _is_input_char_valid(self, x):
        if self._is_item_separator(x) and not self._is_item_separator_expected():
            raise ValueError(f"Empty item")
        return not is_whitespace(x)

    def _is_item_separator_expected(self):
        return self.has_input() or self._just_accepted_output

    def accept_char(self, x):
        if self._is_input_char_valid(x):
            self.is_closed = self.is_closed or self.is_end_char(x)
            if self._is_item_separator(x) or self.is_closed:
                self._parse_input_as_item()
            else:
                self.input.append(x)
            self._just_accepted_output = False

    def accept_item(self, output):
        self.output.append(output)
        self._just_accepted_output = True

    def get_output(self):
        return self.output