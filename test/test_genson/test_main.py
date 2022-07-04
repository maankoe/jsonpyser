import unittest


from genson.main import dump_jsonable


class TestGenson(unittest.TestCase):
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
