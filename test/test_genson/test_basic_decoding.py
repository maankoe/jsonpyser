import unittest

from genson.decoding import decode_json

class TestBasicDecoding(unittest.TestCase):
    def test_decode_empty_string(self):
        self.assertEquals(decode_json('""'), "")

    def test_decode_string(self):
        self.assertEquals(decode_json('"ASDF"'), "ASDF")

    def test_decode_int(self):
        self.assertEquals(decode_json("1"), 1)
        self.assertEquals(decode_json("13"), 13)
        self.assertEquals(decode_json("123"), 123)

    def test_decode_float(self):
        self.assertEquals(decode_json("1.4"), 1.4)
        self.assertEquals(decode_json("10.4"), 10.4)
        self.assertEquals(decode_json("12.45"), 12.45)
        self.assertEquals(decode_json("12."), 12.)

    def test_decode_empty_list(self):
        self.assertEqual(decode_json("[]"), [])

    def test_decode_list_with_int(self):
        self.assertEqual(decode_json("[1]"), [1])