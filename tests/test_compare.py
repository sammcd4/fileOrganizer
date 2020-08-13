import unittest
from fileorganizer.comparator import Comparator
import os
import shutil

class CompareTests(unittest.TestCase):

    move_duplicates = False
    print_output = False
    identical_dir = '../files/identical/'
    different_dir = '../files/different/'
    ignore_extensions = False

    def assertEmpty(self, obj):
        self.assertEqual(len(obj), 0, "Object is not empty")

    def compare_dirs(self, parent_dir, folder1, folder2):
        comp = Comparator(self.move_duplicates, self.print_output, self.ignore_extensions)
        dir1 = parent_dir + folder1
        dir2 = parent_dir + folder2
        self.assertTrue(comp.compare_folders(dir1, dir2))
        return comp

    def compare_identical_dirs(self, folder1, folder2):
        return self.compare_dirs(self.identical_dir, folder1, folder2)

    def compare_different_dirs(self, folder1, folder2):
        return self.compare_dirs(self.different_dir, folder1, folder2)

    def test_empty_directories(self):
        comp = Comparator(self.move_duplicates)
        result = comp.compare_folders('', '')
        self.assertEqual(result, None)

    def test_all_identical(self):

        # Identical files (name and content) compare equal
        comp = self.compare_identical_dirs('dir1', 'dir2')
        dcmp = comp.dcmp

        # if all identical, no unique files in either directory
        self.assertFalse(comp.left_only_found)
        self.assertFalse(comp.right_only_found)

        # all common file names should also be identical
        self.assertEqual(dcmp.common_files, dcmp.same_files)
        self.assertFalse(dcmp.diff_files)

    def test_identical_diffext(self):
        # Setup
        self.ignore_extensions = True

        # Identical files (but different extensions) compare equal
        comp = self.compare_identical_dirs('diffext1', 'diffext2')
        dcmp = comp.dcmp

        # if identical, no unique files in either directory
        # TODO: This is currently passing for the wrong reason. these aren't ever filled
        self.assertEmpty(comp.left_only_found)
        self.assertEmpty(comp.right_only_found)

        # check same number of files in common and same because different extension will make lists unequal
        self.assertEqual(len(dcmp.common_files), len(dcmp.same_files))
        self.assertFalse(dcmp.diff_files)

        # Cleanup
        self.ignore_extensions = False

    def test_identical_diffname(self):

        # Identical files (but different filenames) compare equal
        comp = self.compare_identical_dirs('diffname1', 'diffname2')

        self.assertFalse(comp.left_only_found)
        self.assertFalse(comp.right_only_found)

        self.assertEqual(len(comp.dcmp.common_files), len(comp.dcmp.same_files))
        self.assertFalse(comp.dcmp.diff_files)

    def test_all_diff(self):

        # Different files (name and content) compare not equal
        comp = self.compare_different_dirs('dir1', 'dir2')
        dcmp = comp.dcmp

        # there should be no common files (files of same name) and no same files (identical files)
        self.assertEmpty(dcmp.common_files)
        self.assertEmpty(dcmp.same_files)

    def test_funny_files(self):
        # TODO: Write this with some given funny files
        self.assertEqual(True, True)

    def test_different_filenames(self):
        # TODO: Write this with filenames that are clearly different
        self.assertEqual(True, True)

    def test_diff_same_name(self):
        # Different files (based on content) compare not equal
        comp = self.compare_different_dirs('samename1', 'samename2')
        dcmp = comp.dcmp

        # there should be common files (files of same name) but no same files (identical files)
        self.assertTrue(dcmp.common_files)
        self.assertEmpty(dcmp.same_files)

    def test_diff_diff_name(self):
        # should be covered by test_all_diff
        pass

    def test_diff_same_ext(self):
        # should be covered by test_diff_same_name
        pass

    def test_diff_diff_ext(self):
        pass

    def test_diff_same_filenames(self):

        # Different files with same filenames are actually different
        comp = self.compare_different_dirs('samename1', 'samename2')
        dcmp = comp.dcmp

        # there should be
        self.assertEqual(dcmp.common_files, dcmp.diff_files)
        self.assertFalse(dcmp.same_files)

    def test_move_file(self):
        # actually move an identical test file
        comp = Comparator(True, self.print_output)
        dir1 = self.identical_dir + 'move1'
        dir2 = self.identical_dir + 'dir2'
        self.assertTrue(comp.compare_folders(dir1, dir2))

        # check file exists in comparisons folder
        # TODO: iterate over all files in move1 instead of hard coding here
        filepath = os.path.join(comp.duplicates_dir, 'IMG_0900.JPG')
        self.assertTrue(os.path.isfile(filepath), 'Expected file to be at {}'.format(filepath))

        # Ensure that empty move1 folder was deleted as expected
        self.assertFalse(os.path.isdir(dir1), 'Expected {} to be non-existent'.format(dir1))

        # move the file back to where it came from in move1
        if not os.path.isdir(dir1):
            os.mkdir(dir1)
        move1_filepath = os.path.join(dir1, 'IMG_0900.JPG')
        self.assertFalse(os.path.isfile(move1_filepath))
        shutil.move(filepath, move1_filepath)
        self.assertTrue(os.path.isfile(move1_filepath))

        # No logic so far to remove empty duplicates folder, but in this case it will be empty and need removal
        if os.path.isdir(comp.duplicates_dir):
            os.rmdir(comp.duplicates_dir)

    def test_maintain_file_path(self):
        # Ensure that the original file path is preserved when moving the identical file after comparison
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
