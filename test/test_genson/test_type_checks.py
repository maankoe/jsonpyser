import unittest


from genson.json_typing import *


class TestGenson(unittest.TestCase):
    def test_is_map(self):
        self.assertTrue(is_map({}))
        self.assertTrue(is_map({"a": "b"}))
        self.assertTrue(is_map({"a": 1}))
        self.assertTrue(is_map({2: 1}))
        self.assertTrue(is_map({2: ["a", "b"]}))
        self.assertFalse(is_map("asdf"))
        self.assertFalse(is_map(1))
        self.assertFalse(is_map([1, 2, 3]))
        self.assertFalse(is_map(("a", 1, 2, )))
        self.assertFalse(is_map(("a", {"a": "b"})))

    def test_is_str(self):
        self.assertTrue(is_str("asdf"))
        self.assertFalse(is_str([1, 2, 3]))
        self.assertFalse(is_str(("a", 1, 2,)))
        self.assertFalse(is_str(("a", {"a": "b"})))
        self.assertFalse(is_str({}))
        self.assertFalse(is_str({"a": "b"}))
        self.assertFalse(is_str({"a": 1}))
        self.assertFalse(is_str({2: 1}))
        self.assertFalse(is_str({2: ["a", "b"]}))
        self.assertFalse(is_str(1))

    def test_is_array(self):
        self.assertTrue(is_array([1, 2, 3]))
        self.assertTrue(is_array(("a", 1, 2, )))
        self.assertTrue(is_array(("a", {"a": "b"})))
        self.assertFalse(is_array({}))
        self.assertFalse(is_array({"a": "b"}))
        self.assertFalse(is_array({"a": 1}))
        self.assertFalse(is_array({2: 1}))
        self.assertFalse(is_array({2: ["a", "b"]}))
        self.assertFalse(is_array("asdf"))
        self.assertFalse(is_array(1))

    def test_is_object(self):
        self.assertTrue(is_object("asdf"))
        self.assertTrue(is_object(1))
        self.assertFalse(is_object([1, 2, 3]))
        self.assertFalse(is_object(("a", 1, 2, )))
        self.assertFalse(is_object(("a", {"a": "b"})))
        self.assertFalse(is_object({}))
        self.assertFalse(is_object({"a": "b"}))
        self.assertFalse(is_object({"a": 1}))
        self.assertFalse(is_object({2: 1}))
        self.assertFalse(is_object({2: ["a", "b"]}))

    def test_is_number(self):
        self.assertTrue(is_number(1))
        self.assertTrue(is_number(1.1))
        self.assertTrue(is_number(1.0))
        self.assertFalse(is_number("asdf"))
        self.assertFalse(is_number([1, 2, 3]))
        self.assertFalse(is_number(("a", 1, 2, )))
        self.assertFalse(is_number(("a", {"a": "b"})))
        self.assertFalse(is_number({}))
        self.assertFalse(is_number({"a": "b"}))
        self.assertFalse(is_number({"a": 1}))
        self.assertFalse(is_number({2: 1}))
        self.assertFalse(is_number({2: ["a", "b"]}))

