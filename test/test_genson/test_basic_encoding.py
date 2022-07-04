import unittest


from genson.encoding import dump_jsonable


class TestBasicEncoding(unittest.TestCase):
    def test_returns_string(self):
        self.assertIsInstance(dump_jsonable({}), str)

    def test_empty_dict_json(self):
        self.assertEqual(dump_jsonable({}), "{}")

    def test_empty_list_json(self):
        self.assertEqual(dump_jsonable([]), "[]")

    def test_dump_string_object(self):
        self.assertEqual(dump_jsonable("ASDF"), '"ASDF"')

    def test_dump_number_object(self):
        self.assertEqual(dump_jsonable(5), "5")
        self.assertEqual(dump_jsonable(5.0), "5.0")

    def test_dump_array_with_numbers(self):
        self.assertEqual(dump_jsonable([5, 6.3, 7]), "[5, 6.3, 7]")

    def test_dump_array_with_strings(self):
        self.assertEqual(dump_jsonable(["a", "b", "c"]), '["a", "b", "c"]')

    def test_dump_map_with_number_values(self):
        self.assertEqual(dump_jsonable({"a": 5, "b": 3, "c": 2}), '{"a": 5, "b": 3, "c": 2}')

    def test_dump_map_with_string_values(self):
        self.assertEqual(dump_jsonable({"a": "d", "b": "e", "c": "f"}), '{"a": "d", "b": "e", "c": "f"}')

    def test_dump_map_with_number_string_mix_values(self):
        self.assertEqual(dump_jsonable({"a": "d", "b": 5, "c": "f"}), '{"a": "d", "b": 5, "c": "f"}')

    def test_dump_map_with_list_of_lists(self):
        self.assertEqual(dump_jsonable([[1, 2, 3], ["a", "b", "c"], [7, 8, 9]]),
                         '[[1, 2, 3], ["a", "b", "c"], [7, 8, 9]]')

    def test_dump_map_with_dict_of_list_values(self):
        self.assertEqual(dump_jsonable({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [7, 8, 9]}),
                         '{"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [7, 8, 9]}')

    def test_dump_None(self):
        self.assertEqual(dump_jsonable(None), "null")