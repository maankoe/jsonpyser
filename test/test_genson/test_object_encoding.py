import dataclasses
import unittest
from dataclasses import dataclass

from genson.encoding import dump_jsonable


class_open = "<"
class_close = ">"

class TestObjectEncoding(unittest.TestCase):
    def test_encode_object_via_repr(self):
        class A:
            def __init__(self, data):
                self.data = data
            def __repr__(self):
                return f"{type(self).__name__}('{self.data}')"

        jsonable = A("Hello world")
        expected = f"{class_open}A('Hello world'){class_close}"
        self.assertEqual(dump_jsonable(jsonable), expected)

    def test_encode_dataclass(self):
        @dataclass
        class A:
            data: str

        dataclass_name = A.__qualname__
        jsonable = A("Hello world")
        expected = f"{class_open}{dataclass_name}(data='Hello world'){class_close}"
        self.assertEqual(dump_jsonable(jsonable), expected)
