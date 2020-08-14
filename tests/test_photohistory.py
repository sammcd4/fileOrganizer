import unittest
from photohistory import get_types_from_folder


class PhotoHistoryTests(unittest.TestCase):

    print_output = False # TODO: actually use this, like photohistory class
    dir1 = '../files/identical/dir1'

    def assert_type_count(self, types_dict, type, count):
        self.assertEqual(types_dict['livephotovideo']['count'], 3)

    def test_single_dir(self):
        types_dict = get_types_from_folder(self.dir1)

        self.assert_type_count(types_dict, 'photo', 2)
        self.assert_type_count(types_dict, 'video', 1)
        self.assert_type_count(types_dict, 'livephoto', 3)
        self.assert_type_count(types_dict, 'livephotovideo', 3)

    def test_nested_dir(self):
        types_dict = get_types_from_folder()


if __name__ == '__main__':
    unittest.main()