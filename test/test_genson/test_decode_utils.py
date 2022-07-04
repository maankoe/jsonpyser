import unittest

from genson.decoding_utils import *

class TestDecodeUtils(unittest.TestCase):
    def test_is_whitespace(self):
        self.assertTrue(is_whitespace(" "))
        self.assertTrue(is_whitespace("\t"))
        self.assertTrue(is_whitespace("    "))
        self.assertTrue(is_whitespace("\t\t\t"))
        self.assertTrue(is_whitespace(" \t \t\t  \t"))
        self.assertFalse(is_whitespace("a"))
        self.assertFalse(is_whitespace("'"))
        self.assertFalse(is_whitespace("\\"))
        self.assertFalse(is_whitespace("[]"))

    def test_is_escape(self):
        self.assertTrue(is_escape("\\"))
        self.assertFalse(is_escape("\\\\"))
        self.assertFalse(is_escape("\t"))
        self.assertFalse(is_escape("\""))
        self.assertFalse(is_escape(" "))
        self.assertFalse(is_escape("a"))
        self.assertFalse(is_escape("["))

    def test_is_int(self):
        self.assertTrue(is_int_match("1"))
        self.assertTrue(is_int_match("123"))
        self.assertFalse(is_int_match(" 1"))
        self.assertFalse(is_int_match("1 "))
        self.assertFalse(is_int_match(" 1 "))
        self.assertFalse(is_int_match("1 23"))
        self.assertFalse(is_int_match("1.23"))
        self.assertFalse(is_int_match(" .23"))

    def test_is_float(self):
        self.assertTrue(is_float_match("1"))
        self.assertTrue(is_float_match("123"))
        self.assertTrue(is_float_match("1.23"))
        self.assertTrue(is_float_match(".23"))
        self.assertFalse(is_float_match(" 1"))
        self.assertFalse(is_float_match("1 "))
        self.assertFalse(is_float_match(" 1 "))
        self.assertFalse(is_float_match("1 23"))
        self.assertFalse(is_float_match(" .23"))

    def test_decode_item_int(self):
        self.assertIs(decode_item("1"), int(1))
        self.assertIs(decode_item("123"), int(123))

    def test_decode_item_float(self):
        self.assertAlmostEqual(decode_item("1.23"), float(1.23))
        self.assertAlmostEqual(decode_item(".23"), float(0.23))

    def test_bad_inputs(self):
        for input_str in [" 1", " 1 ", "1 23", " .23"]:
            with self.assertRaisesRegex(ValueError, "Unrecognised item"):
                decode_item(input_str)