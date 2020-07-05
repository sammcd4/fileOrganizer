import unittest
from fileorganizer.comparator import Comparator


class MyTestCase(unittest.TestCase):

    move_duplicates = False
    print_output = False
    identical_dir = '../files/identical/'
    different_dir = '../files/different/'

    def assertEmpty(self, obj):
        self.assertEqual(len(obj), 0, "Object is not empty")

    def compare_dirs(self, dir1, dir2):
        comp = Comparator(self.move_duplicates)
        return comp.compare_folders(dir1, dir2)

    def test_empty_directories(self):
        comp = Comparator(self.move_duplicates)
        result = comp.compare_folders('', '')
        self.assertEqual(result, None)

    def test_all_identical(self):

        # Identical files (name and content) compare equal
        comp = Comparator(self.move_duplicates, self.print_output)
        dir1 = self.identical_dir + 'dir1'
        dir2 = self.identical_dir + 'dir2'
        self.assertTrue(comp.compare_folders(dir1, dir2))

        self.assertFalse(comp.left_only_found)
        self.assertFalse(comp.right_only_found)

        self.assertEqual(comp.dcmp.common_files, comp.dcmp.same_files)
        self.assertFalse(comp.dcmp.diff_files)

    def test_identical_diffext(self):

        # Identical files (name and content) compare equal
        comp = Comparator(self.move_duplicates, self.print_output)
        dir1 = self.identical_dir + 'diffext1'
        dir2 = self.identical_dir + 'diffext2'
        self.assertTrue(comp.compare_folders(dir1, dir2))

        self.assertEmpty(comp.left_only_found)
        self.assertEmpty(comp.right_only_found)

        self.assertEqual(len(comp.dcmp.common_files), len(comp.dcmp.same_files))
        self.assertFalse(comp.dcmp.diff_files)

    def test_identical_diffname(self):

        # Identical files (name and content) compare equal
        comp = Comparator(self.move_duplicates, self.print_output)
        dir1 = self.identical_dir + 'diffname1'
        dir2 = self.identical_dir + 'diffname2'
        self.assertTrue(comp.compare_folders(dir1, dir2))

        self.assertFalse(comp.left_only_found)
        self.assertFalse(comp.right_only_found)

        self.assertEqual(len(comp.dcmp.common_files), len(comp.dcmp.same_files))
        self.assertFalse(comp.dcmp.diff_files)

    def test_all_diff(self):

        # Different files (name and content) compare not equal
        comp = Comparator(self.move_duplicates, self.print_output)
        dir1 = self.different_dir + 'dir1'
        dir2 = self.different_dir + 'dir2'
        self.assertTrue(comp.compare_folders(dir1, dir2))

        self.assertEqual(comp.dcmp.common_files, comp.dcmp.same_files)
        self.assertFalse(comp.dcmp.same_files)

    def test_funny_files(self):
        self.assertEqual(True, True)

    def test_different_filenames(self):
        self.assertEqual(True, True)

    def test_diff_same_filenames(self):

        # Different files with same filenames are actually different
        comp = Comparator(self.move_duplicates, self.print_output)
        dir1 = self.different_dir + 'samename1'
        dir2 = self.different_dir + 'samename2'
        self.assertTrue(comp.compare_folders(dir1, dir2))

        self.assertEqual(comp.dcmp.common_files,
                         comp.dcmp.diff_files)
        self.assertFalse(comp.dcmp.same_files)


if __name__ == '__main__':
    unittest.main()
