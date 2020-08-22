import unittest
import fileorganizer.utils as utils


class UtilsTests(unittest.TestCase):

    print_output = False

    def assertEmpty(self, obj):
        self.assertEqual(len(obj), 0, "Object is not empty")

    def assertExtensionVariations(self, extensions, **kargs):
        for ext in extensions:
            self.assertCountEqual(utils.get_extension_variations(ext), extensions, kargs)

    def test_get_extension_variations(self):
        photo_ext = ['.JPG', '.jpg', '.jpeg', '.JPEG']
        self.assertExtensionVariations(photo_ext)

        mov_ext = ['.mov', '.MOV']
        self.assertExtensionVariations(mov_ext)
        avi_ext = ['.avi', '.AVI']
        self.assertExtensionVariations(avi_ext)
        mpg_ext = ['.mpg', '.MPG', '.mpeg', '.MPEG']
        self.assertExtensionVariations(mpg_ext)
        m4v_ext = ['.m4v', '.M4V']
        self.assertExtensionVariations(m4v_ext)
        mp4_ext = ['.mp4', '.MP4']
        self.assertExtensionVariations(mp4_ext)

        # TODO: Need more extensions to verify
        #livephoto_ext = ['LivePhoto.jpg', 'LivePhoto.JPEG', 'LivePhoto.JPG', 'LivePhoto.jpeg', 'LivePhoto.heic', 'LivePhoto.HEIC']
        #self.assertExtensionVariations(livephoto_ext, prepend='LivePhoto')

    def test_get_extensions_from_type(self):
        photo_exts = ['.JPG','.jpg', '.jpeg', '.JPEG']
        self.assertCountEqual(utils.get_extension_variations('.jpg'), utils.get_extensions_from_type('photo'))

        video_exts = ['.mov', '.MOV', '.AVI', '.avi', '.mpg', '.MPG', '.mpeg', '.MPEG', '.m4v', '.M4V', '.mp4', '.MP4']
        self.assertCountEqual(video_exts, utils.get_extensions_from_type('video'))

        livephoto_exts = ['LivePhoto.jpg', 'LivePhoto.JPEG', 'LivePhoto.JPG', 'LivePhoto.jpeg', 'LivePhoto.heic', 'LivePhoto.HEIC']
        self.assertCountEqual(livephoto_exts, utils.get_extensions_from_type('livephoto'))

        livephotovideo_exts = ['LivePhoto.mov', 'LivePhoto.MOV']
        self.assertCountEqual(livephotovideo_exts, utils.get_extensions_from_type('livephotovideo'))

        screenshot_exts = ['.png', '.PNG']
        self.assertCountEqual(screenshot_exts, utils.get_extensions_from_type('screenshot'))

        raw_exts = ['.cr2', '.CR2']
        self.assertCountEqual(raw_exts, utils.get_extensions_from_type('raw'))

    def test_get_extensions(self):
        self.assertEqual(utils.get_extensions('../files/identical/diffext1'), ['.JPEG', '.JPG'])
        self.assertEqual(utils.get_extensions('../files/identical/dir1'), ['.JPG', '.mp4', '.mov'])
        # TODO: Should the order matter?

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
        self.assertEqual(utils.get_convertible_extensions('.blah'), ['.BLAH'])


if __name__ == '__main__':
    unittest.main()
