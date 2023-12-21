import unittest
from photohistory import get_types_from_folder, DateRange
import fileorganizer.utils as utils
import os


class PhotoHistoryTests(unittest.TestCase):

    print_output = False # TODO: actually use this, like photohistory class

    def __init__(self, *args, **kwargs):
        super(PhotoHistoryTests, self).__init__(*args, **kwargs)

        # initialize identical and different directories relative to working directory chosen by test runner
        current_pathname = os.path.basename(os.path.normpath(os.getcwd()))
        if current_pathname == 'fileOrganizer':
            # test runner is running from project directory
            self.project_dir = ''

        elif current_pathname == 'tests':
            # test runner is running from where this file lives
            self.project_dir = '../'

        self.identical_dir = self.project_dir + 'files/identical/'
        self.dir1 = self.identical_dir + 'dir1'
        self.nested_dir1 = self.identical_dir + 'nested_dir1'
        self.init_file = self.project_dir + 'types_init.xls'

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

        # TODO: Recalculate type count by counting individual sub directories
        sub_dirs = utils.get_sub_dirs(self.nested_dir1)
        types_dict_sub1 = get_types_from_folder(self.nested_dir1)

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

    def test_init_file(self):
        types_dict = get_types_from_folder(self.identical_dir, drill_down=False, init_file=self.init_file, init_row_idx=1)

        self.assert_type_count(types_dict, 'applephoto', 1)
        self.assert_type_count(types_dict, 'livephoto', 3)

        types_dict = get_types_from_folder(self.identical_dir, drill_down=False, init_file=self.init_file,
                                           init_row_idx=2)

        self.assert_type_count(types_dict, 'applephoto', 5)
        self.assert_type_count(types_dict, 'livephoto', 7)


if __name__ == '__main__':
    unittest.main()