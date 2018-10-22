'''
Main functionality of ``image_slicer``.
'''
import os
from math import sqrt, ceil, floor

from PIL import Image

from .helpers import get_basename


class Tile(object):
    """Represents a single tile."""

    def __init__(self, image, number, position, coords, filename=None):
        self.image = image
        self.number = number
        self.position = position
        self.coords = coords
        self.filename = filename

    @property
    def row(self):
        return self.position[0]

    @property
    def column(self):
        return self.position[1]

    @property
    def basename(self):
        """Strip path and extension. Return base filename."""
        return get_basename(self.filename)

    def generate_filename(self, directory=os.getcwd(), prefix='tile',
                          format='png', path=True):
        """Construct and return a filename for this tile."""
        filename = prefix + '_{col:02d}_{row:02d}.{ext}'.format(
                      col=self.column, row=self.row, ext=format.lower().replace('jpeg', 'jpg'))
        if not path:
            return filename
        return os.path.join(directory, filename)

    def save(self, filename=None, format='png'):
        if not filename:
            filename = self.generate_filename(format=format)
        self.image.save(filename, format)
        self.filename = filename

    def __repr__(self):
        """Show tile number, and if saved to disk, filename."""
        if self.filename:
            return '<Tile #{} - {}>'.format(self.number,
                                            os.path.basename(self.filename))
        return '<Tile #{}>'.format(self.number)


def calc_columns_rows(n):
    """
    Calculate the number of columns and rows required to divide an image
    into ``n`` parts.

    Return a tuple of integers in the format (num_columns, num_rows)
    """
    num_columns = int(ceil(sqrt(n)))
    num_rows = int(ceil(n / float(num_columns)))
    return (num_columns, num_rows)

def get_combined_size(tiles):
    """Calculate combined size of tiles."""
    # TODO: Refactor calculating layout to avoid repetition.
    columns, rows = calc_columns_rows(len(tiles))
    tile_size = tiles[0].image.size
    return (tile_size[0] * columns, tile_size[1] * rows)

def join(tiles):
    """
    @param ``tiles`` - Tuple of ``Image`` instances.
    @return ``Image`` instance.
    """
    im = Image.new('RGB', get_combined_size(tiles), None)
    columns, rows = calc_columns_rows(len(tiles))
    for tile in tiles:
        im.paste(tile.image, tile.coords)
    return im

def validate_image(image, number_tiles):
    """Basic sanity checks prior to performing a split."""
    TILE_LIMIT = 99 * 99

    try:
        number_tiles = int(number_tiles)
    except:
        raise ValueError('number_tiles could not be cast to integer.')

    if number_tiles > TILE_LIMIT or number_tiles < 2:
        raise ValueError('Number of tiles must be between 2 and {} (you \
                          asked for {}).'.format(TILE_LIMIT, number_tiles))

def slice(filename, number_tiles, save=True):
    """
    Split an image into a specified number of tiles.

    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.

    Kwargs:
       save (bool): Whether or not to save tiles to disk.

    Returns:
        Tuple of :class:`Tile` instances.
    """
    im = Image.open(filename)
    validate_image(im, number_tiles)

    im_w, im_h = im.size
    columns, rows = calc_columns_rows(number_tiles)
    extras = (columns * rows) - number_tiles
    tile_w, tile_h = int(floor(im_w / columns)), int(floor(im_h / rows))

    tiles = []
    number = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(floor(pos_x / tile_w)) + 1,
                        int(floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1
    if save:
        save_tiles(tiles,
                   prefix=get_basename(filename),
                   directory=os.path.dirname(filename))
    return tuple(tiles)

def save_tiles(tiles, prefix='', directory=os.getcwd(), format='png'):
    """
    Write image files to disk. Create specified folder(s) if they
       don't exist. Return list of :class:`Tile` instance.

    Args:
       tiles (list):  List, tuple or set of :class:`Tile` objects to save.
       prefix (str):  Filename prefix of saved tiles.

    Kwargs:
       directory (str):  Directory to save tiles. Created if non-existant.

    Returns:
        Tuple of :class:`Tile` instances.
    """
#    Causes problems in CLI script.
#    if not os.path.exists(directory):
#        os.makedirs(directory)
    for tile in tiles:
        tile.save(filename=tile.generate_filename(prefix=prefix,
                                                  directory=directory,
                                                  format=format), 
                                                  format=format)
    return tuple(tiles)

