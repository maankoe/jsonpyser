import unittest

from genson.decoding import decode_json

class TestStringDecoding(unittest.TestCase):
    def test_decode_empty_string(self):
        self.assertEqual(decode_json('""'), "")

    def test_decode_empty_string_in_array(self):
        self.assertEqual(decode_json('[""]'), [""])

    def test_string_context(self):
        self.assertEqual(decode_json('"hello world"'), "hello world")
        self.assertEqual(decode_json('["hello world"]'), ["hello world"])

    def test_unclosed_string(self):
        with self.assertRaisesRegex(ValueError, "unclosed context"):
            decode_json('"hello world')

    def test_unclosed_string_in_array(self):
        with self.assertRaisesRegex(ValueError, "unclosed context"):
            decode_json('["hello","]')

    def test_extra_string_close(self):
        with self.assertRaisesRegex(ValueError, "Extra characters"):
            decode_json('"hello""')

    def test_string_opening_other_context(self):
        self.assertEqual(decode_json('"hello[world"'), "hello[world")

    def test_string_escape(self):
        self.assertEqual(decode_json('"hello\\"world"'), "hello\"world")

    def test_string_escaped_escape(self):
        self.assertEqual(decode_json('"hello\\\\world"'), "hello\\world")