import unittest


from genson.json_typing import *


class TestGenson(unittest.TestCase):
    def test_is_dict(self):
        self.assertTrue(is_dict({}))
        self.assertTrue(is_dict({"a": "b"}))
        self.assertTrue(is_dict({"a": 1}))
        self.assertTrue(is_dict({2: 1}))
        self.assertTrue(is_dict({2: ["a", "b"]}))
        self.assertFalse(is_dict("asdf"))
        self.assertFalse(is_dict(1))
        self.assertFalse(is_dict([1, 2, 3]))
        self.assertFalse(is_dict(("a", 1, 2, )))
        self.assertFalse(is_dict(("a", {"a": "b"})))

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

    def test_is_int(self):
        self.assertTrue(is_int(1))
        self.assertFalse(is_int("asdf"))
        self.assertFalse(is_int([1, 2, 3]))
        self.assertFalse(is_int(("a", 1, 2, )))
        self.assertFalse(is_int(("a", {"a": "b"})))
        self.assertFalse(is_int({}))
        self.assertFalse(is_int({"a": "b"}))
        self.assertFalse(is_int({"a": 1}))
        self.assertFalse(is_int({2: 1}))
        self.assertFalse(is_int({2: ["a", "b"]}))

