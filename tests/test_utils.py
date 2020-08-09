import unittest
import fileorganizer.utils as utils


class UtilsTests(unittest.TestCase):

    print_output = False

    def assertEmpty(self, obj):
        self.assertEqual(len(obj), 0, "Object is not empty")

    def test_get_extensions(self):
        # TODO: Need to implement get_extensions
        self.assertTrue(False)

    def test_get_convertible_extensions(self):
        self.assertEqual(utils.get_convertible_extensions('.JPG'), ['.jpg', '.jpeg', '.JPEG'])
        self.assertEqual(utils.get_convertible_extensions('.jpg'), ['.JPG', '.jpeg', '.JPEG'])
        self.assertEqual(utils.get_convertible_extensions('.jpeg'), ['.JPG', '.jpg', '.JPEG'])
        self.assertEqual(utils.get_convertible_extensions('.JPEG'), ['.jpg', '.JPG', '.jpeg'])
        self.assertEqual(utils.get_convertible_extensions('.mov'), ['.MOV'])
        self.assertEqual(utils.get_convertible_extensions('.MOV'), ['.mov'])
        self.assertEqual(utils.get_convertible_extensions('.heic'), ['.HEIC'])
        self.assertEqual(utils.get_convertible_extensions('.HEIC'), ['.heic'])
        self.assertEqual(utils.get_convertible_extensions('.MPG'), ['.mpg', '.mpeg', '.MPEG'])
        self.assertEqual(utils.get_convertible_extensions('.mpg'), ['.MPG', '.mpeg', '.MPEG'])
        self.assertEqual(utils.get_convertible_extensions('.mpeg'), ['.mpg', '.MPG', '.MPEG'])
        self.assertEqual(utils.get_convertible_extensions('.MPEG'), ['.MPG', '.mpg', '.mpeg'])
        self.assertEqual(utils.get_convertible_extensions('.mp4'), ['.MP4'])
        self.assertEqual(utils.get_convertible_extensions('.MP4'), ['.mp4'])
        self.assertEqual(utils.get_convertible_extensions('.png'), ['.PNG'])
        self.assertEqual(utils.get_convertible_extensions('.PNG'), ['.png'])

        # no match
        self.assertEqual(utils.get_convertible_extensions('.blah'), [])

if __name__ == '__main__':
    unittest.main()
