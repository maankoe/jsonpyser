import unittest


from genson.main import dumps


class TestGenson(unittest.TestCase):
    def test_returns_string(self):
        self.assertIsInstance(dumps({}), str)

    def test_empty_dict_json(self):
        self.assertEqual(dumps({}), "{}")

    def test_empty_list_json(self):
        self.assertEqual(dumps([]), "[]")

    def test_dump_string_object(self):
        self.assertEqual(dumps("ASDF"), '"ASDF"')

    def test_dump_number_object(self):
        self.assertEqual(dumps(5), "5")
        self.assertEqual(dumps(5.0), "5.0")