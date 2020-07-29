import unittest
from photohistory import get_types_from_folder


class PhotoHistoryTests(unittest.TestCase):

    print_output = False # TODO: actually use this, like photohistory class
    dir1 = '../files/identical/dir1'

    def test_simple(self):
        types_dict = get_types_from_folder(self.dir1)

        self.assertEqual(types_dict['photo']['count'], 3)
        self.assertEqual(types_dict['livephoto']['count'], 3)


if __name__ == '__main__':
    unittest.main()