'''
Main functionality of ``image_slicer``.
'''
import os
from math import sqrt, ceil

from PIL import Image

from .helpers import get_basename


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
    tile_size = tiles[0].size
    return (tile_size[0] * columns, tile_size[1] * rows)

def join_tiles(tiles):
    """
    @param ``tiles`` - Tuple of ``Image`` instances.
    @return ``Image`` instance.
    """
    im = Image.new('RGB', get_combined_size(tiles), None)
    columns, rows = calc_columns_rows(len(tiles))
    for tile in tiles:
        im.paste(tile, tile.position)
    return im

def validate_image(image, num_tiles):
    """Basic sanity checks prior to performing a split."""
    TILE_LIMIT = 99 * 99
    if num_tiles > TILE_LIMIT or num_tiles < 2:
        raise ValueError('Number of tiles must be between 2 and {0} (you \
                          asked for {1}).'.format(TILE_LIMIT, num_tiles))

def split_image(filename, num_tiles, save=True):
    """
    Split an image into a specified number of tiles.

    Args:
       filename (str):  The filename of the image to split.
       num_tiles (int):  The number of tiles required.

    Kwargs:
       save (bool): Whether or not to save tiles to disk.

    Returns:
        *if ``save=True`` (default):*
            Tuple of filenames of the saved tiles.
        *if ``save=False``:*
            Tuple of ``Image`` instances.
    """
    # Needs tests.
    basename = get_basename(filename)
    im = Image.open(filename)
    validate_image(im, num_tiles)

    im_w, im_h = im.size
    columns, rows = calc_columns_rows(num_tiles)
    extras = (columns * rows) - num_tiles
    tile_w, tile_h = int(im_w / columns), int(im_h / rows)

    tiles = []
    num = 1
    for pos_y in range(0, im_h - rows, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w - columns, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            tile = im.crop(area)
            tile.id = ((pos_x / tile_w) + 1, (pos_y / tile_h) + 1)
            tile.position = (pos_x, pos_y)
            tiles.append(tile)
            num += 1
    if save:
        save_tiles(tiles, prefix=basename)
    return tiles

def save_tiles(tiles, prefix='', directory='.', ext='png'):
    """Write image files to disk."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    tile_filenames = []
    for tile in tiles:
        row, column = tile.id[0], tile.id[1]
        filename = os.path.join(directory, prefix +\
                                '_{col:02d}_{row:02d}.{ext}'.format(
                                col=column, row=row, ext=ext))
        tile.save(filename)
        tile_filenames.append(filename)
    return tile_filenames

