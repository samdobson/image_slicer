from __future__ import with_statement
import unittest

from image_slicer import *


TEST_IMAGE = os.path.join(os.path.dirname(__file__), 'sample.jpg')
TEST_DIR = os.path.join(os.path.dirname(__file__), 'test_output')
NUMBER_TILES = 20


class SaveOpenTest(unittest.TestCase):

    def setUp(self):
        self.tiles = slice(TEST_IMAGE, NUMBER_TILES, save=False)
        os.mkdir(TEST_DIR)

    def tearDown(self):
        for file in os.listdir(TEST_DIR):
            os.remove(os.path.join(TEST_DIR, file))
        os.rmdir(TEST_DIR)

    def test_all_files_saved(self):
        save_tiles(self.tiles, prefix='x', directory=TEST_DIR, format='gif')
        self.assertEqual(sorted(os.listdir(TEST_DIR)),
 ['x_01_01.gif', 'x_01_02.gif', 'x_01_03.gif', 'x_01_04.gif', 'x_01_05.gif',
  'x_02_01.gif', 'x_02_02.gif', 'x_02_03.gif', 'x_02_04.gif', 'x_02_05.gif',
  'x_03_01.gif', 'x_03_02.gif', 'x_03_03.gif', 'x_03_04.gif', 'x_03_05.gif',
  'x_04_01.gif', 'x_04_02.gif', 'x_04_03.gif', 'x_04_04.gif', 'x_04_05.gif']
        )


class GeneralTest(unittest.TestCase):

    def test_get_columns_rows_filenames(self):
        filenames = ['abc_01_01.jpg', 'abc_01_02.jpg',
                     'abc_02_01.jpg', 'abc_02_02.jpg'
                    ]
        self.assertEqual(get_columns_rows(filenames), (2, 2))

        filenames = ['xYz--01_01.bmp', 'xYz--01_02.bmp', 'xYz--01_03.bmp',
                     'xYz--02_01.bmp', 'xYz--02_02.bmp', 'xYz--01_03.bmp',
                     'xYz--03_01.bmp', 'xYz--03_02.bmp', 'xYz--03_03.bmp',
                     'xYz--04_01.bmp', 'xYz--04_02.bmp', 'xYz--04_03.bmp',
                    ]
        self.assertEqual(get_columns_rows(filenames), (3, 4))

        filenames = ['01_01.png', '01_02.png', '01_03.png', '01_04.png',
                     '02_01.png', '02_02.png', '01_03.png', '02_04.png',
                     '03_01.png', '03_02.png', '03_03.png', '03_04.png',
                     '04_01.png', '04_02.png', '04_03.png', '04_04.png',
                     '05_01.png', '05_02.png', '05_03.png', '05_04.png',
                     '06_01.png', '06_02.png', '06_03.png', '06_04.png',
                    ]
        self.assertEqual(get_columns_rows(filenames), (4, 6))


    def test_calc_columns_rows(self):

        def extras(n, columns_rows):
            return (columns_rows[0] * columns_rows[1]) - n

        n = 9
        expected = (3, 3)
        r = calc_columns_rows(n)
        self.assertEqual(r, expected)
        self.assertEqual(extras(n, r), 0)

        n = 75
        expected = (9, 9)
        r = calc_columns_rows(n)
        self.assertEqual(r, expected)
        self.assertEqual(extras(n, r), 6)


class SplitTest(unittest.TestCase):

    def setUp(self):
        self.tiles = slice(TEST_IMAGE, NUMBER_TILES, save=False)

# Broken test in 2.6
#    def test_validate_image(self):
#        for bad_argument in (-1, 0, 1, 12000):
#            with self.assertRaises(ValueError):
#                validate_image(TEST_IMAGE, bad_argument)
#                print("{0} didn't throw an exception".format(bad_argument))

    def test_number_tiles_generated(self):
        rows, columns = calc_columns_rows(NUMBER_TILES)
        number_tiles_generated = rows * columns
        self.assertEqual(len(self.tiles), number_tiles_generated)

    def test_tiles_are_images(self):
        self.assertTrue(all(tile.image.__class__.__name__ == '_ImageCrop')\
                            for tile in self.tiles)

    def test_tile_size_equality(self):
        tile_sizes = (tile.image.size for tile in self.tiles)
        self.assertTrue(len(set(tile_sizes)) <= 1)

"""
class JoinTest(unittest.TestCase):

    def setUp(self):
        self.image = join(open_images(TEST_DIR))

    def test_single_image_created(self):
        self.assertTrue(self.im.__class__.__name__ == 'Image')
"""

class IntegrationTest(unittest.TestCase):

    def setUp(self):
        self.original = Image.open(TEST_IMAGE)
        self.reconstituted = join(slice(TEST_IMAGE, NUMBER_TILES,
                                                    save=False))

    def test_image_size_equality(self):
        width_difference = abs(self.original.size[0] -\
                               self.reconstituted.size[0])
        height_difference = abs(self.original.size[1] -\
                                self.reconstituted.size[1])
        THRESHOLD = 2 # Error margin (px).
        self.assertTrue(width_difference <= THRESHOLD,
                       'Width is {0} pixels out'.format(width_difference))
        self.assertTrue(height_difference <= THRESHOLD,
                       'Height is {0} pixels out'.format(height_difference))

    def test_image_similarity(self):
        total_pixels = self.original.size[0] * self.original.size[1]
        bad_pixels = len(set(self.original.histogram()) ^\
                         set(self.reconstituted.histogram()))
        accuracy = 1 - (float(bad_pixels) / float(total_pixels))
        THRESHOLD = 0.999
        self.assertTrue(accuracy > THRESHOLD,
                  'Images are only {0:.2f}% similar'.format(accuracy * 100))

if __name__ == "__main__":
    unittest.main()

