import re
import unittest

from genson.decoding import decode_json

class TestBasicDecoding(unittest.TestCase):
    def test_decode_empty_string(self):
        self.assertEqual(decode_json('""'), "")

    def test_decode_string(self):
        self.assertEqual(decode_json('"ASDF"'), "ASDF")

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

    def test_decode_empty_list(self):
        self.assertEqual(decode_json("[]"), [])
        self.assertEqual(decode_json(" []"), [])
        self.assertEqual(decode_json("[] "), [])
        self.assertEqual(decode_json("[ ] "), [])
        self.assertEqual(decode_json(" [  ] "), [])

    def test_decode_list_with_int(self):
        self.assertEqual(decode_json("[1]"), [1])

    def test_decode_list_with_multiple_ints(self):
        self.assertEqual(decode_json("[1, 2, 3]"), [1, 2, 3])
        self.assertEqual(decode_json("[1,2,3]"), [1, 2, 3])
        self.assertEqual(decode_json("[1,2 , 3]"), [1, 2, 3])

    def test_decode_nested_int_list(self):
        self.assertEqual(decode_json("[[1, 2], [3, 4], 5]"), [[1, 2], [3, 4], 5])

    def test_decode_double_nested_int_list(self):
        self.assertEqual(decode_json("[[1, [2, 3], 4], [3, 4], 5]"), [[1, [2, 3], 4], [3, 4], 5])

    def test_bad_unclosed_list(self):
        with self.assertRaisesRegex(ValueError, "Unclosed bracket"):
            decode_json("[1,2")

    def test_bad_unclosed_list_with_inner_closed_at_end(self):
        with self.assertRaisesRegex(ValueError, "Unclosed bracket"):
            decode_json("[1,[2,3]")

    def test_mismatching_brace(self):
        with self.assertRaisesRegex(ValueError, "Unclosed bracket"):
            decode_json("[1,[2,3]}")

    def test_extra_closing(self):
        with self.assertRaisesRegex(ValueError, "Extra characters outside context"):
            decode_json("[1,[2,3]]]")

    def test_double_comma(self):
        with self.assertRaisesRegex(ValueError, "Empty item"):
            decode_json("[1,,3]")