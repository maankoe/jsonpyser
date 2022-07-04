import re
import unittest

from genson.decoding import decode_json

class TestNumberDecoding(unittest.TestCase):
    def test_decode_int(self):
        self.assertEqual(decode_json("1"), 1)
        self.assertEqual(decode_json("1 "), 1)
        self.assertEqual(decode_json(" 13"), 13)
        self.assertEqual(decode_json("123"), 123)

    def test_decode_float(self):
        self.assertEqual(decode_json("1.4"), 1.4)
        self.assertEqual(decode_json("10.4 "), 10.4)
        self.assertEqual(decode_json(" 12.45"), 12.45)
        self.assertEqual(decode_json("12."), 12.)




