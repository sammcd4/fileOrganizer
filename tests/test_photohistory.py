import unittest
from photohistory import get_types_from_folder, DateRange


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

    def test_date_range(self):
        # Not in range
        date_range = DateRange(year=2020, month='February')
        types_dict = get_types_from_folder(self.dir1, date_range=date_range)

        self.assert_type_count(types_dict, 'photo', 0)
        self.assert_type_count(types_dict, 'video', 0)
        self.assert_type_count(types_dict, 'livephoto', 0)
        self.assert_type_count(types_dict, 'livephotovideo', 0)

        # In range
        date_range = DateRange(year=2020, month='March')
        types_dict = get_types_from_folder(self.dir1, date_range=date_range)

        self.assert_type_count(types_dict, 'photo', 2)
        self.assert_type_count(types_dict, 'video', 1)
        self.assert_type_count(types_dict, 'livephoto', 3)
        self.assert_type_count(types_dict, 'livephotovideo', 3)

    def test_use_earlier_modified_time(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()