import unittest
from photohistory import get_types_from_folder


class PhotoHistoryTests(unittest.TestCase):

    print_output = False # TODO: actually use this, like photohistory class
    dir1 = '../files/identical/dir1'
    nested_dir1 = '../files/identical/nested_dir1'

    def assert_type_count(self, types_dict, type, count):
        self.assertEqual(types_dict[type]['count'], count,
                         msg='Expected # {}: {}. Actual #: {}'.format(type, count, types_dict[type]['count']))

    def test_single_dir(self):
        types_dict = get_types_from_folder(self.dir1)

        self.assert_type_count(types_dict, 'photo', 2)
        self.assert_type_count(types_dict, 'video', 1)
        self.assert_type_count(types_dict, 'livephoto', 3)
        self.assert_type_count(types_dict, 'livephotovideo', 3)

    def test_nested_dir(self):
        types_dict = get_types_from_folder(self.nested_dir1)

        self.assert_type_count(types_dict, 'photo', 2)
        self.assert_type_count(types_dict, 'video', 1)
        self.assert_type_count(types_dict, 'livephoto', 3)
        self.assert_type_count(types_dict, 'livephotovideo', 3)


if __name__ == '__main__':
    unittest.main()