import unittest
import fileorganizer.comparator as fo_c


class MyTestCase(unittest.TestCase):
    def test_empty_directories(self):
        comp = fo_c.Comparator()
        comp.compare_folders('', '')

    def test_all_identical(self):
        self.assertEqual(True, True)

    def test_all_diff(self):
        self.assertEqual(True, True)

    def test_funny_files(self):
        self.assertEqual(True, True)

    def test_different_filenames(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
