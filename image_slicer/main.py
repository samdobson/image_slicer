import sys
import time
import os
import random
from math import sqrt, ceil

from PIL import Image


def get_prefix(filename):
    """Strip extension to leave only the filename."""
    return os.path.splitext(filename)[0]

def open_images(directory):
    """Open all images in a directory. Return tuple of Image instances."""
    return [Image.open(file) for file in os.listdir(directory)]

def calc_columns_rows(n):
    """
    Use integer ``n`` to calculate the number of columns and rows required.
    Return a tuple of integers in the format (num_columns, num_rows)
    """
    num_columns = int(ceil(sqrt(n)))
    num_rows = int(ceil(n / float(num_columns)))
    return (num_columns, num_rows)

def get_columns_rows(filenames):
    """Derive number of columns and rows from filenames."""
    tiles = []
    for filename in filenames:
        row, column = os.path.splitext(filename)[0][-5:].split('_')
        tiles.append((int(row), int(column)))
    rows = [pos[0] for pos in tiles]; columns = [pos[1] for pos in tiles]
    num_rows = max(rows); num_columns = max(columns)
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
    """Basic sanity checks before performing a split."""
    # TODO: Needs tests.
    TILE_LIMIT = 99 * 99
    if num_tiles > TILE_LIMIT:
        raise ValueError('Maximum number of tiles: {0}'.format(TILE_LIMIT))

def split_image(filename, num_tiles):
    """
    Split an image into a specified number of tiles.
    Return a tuple of ``_ImageCrop`` instances.
    """
    # Needs tests.
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
    return tiles

def save_tiles(tiles, prefix='', directory='./', format='png'):
    """Write image files to disk."""
    filenames = list()
    for tile in tiles:
        row, column = tile.id[0], tile.id[1]
        filename = prefix + '%02d_%02d.%s' % (row, column, format)
        if not os.path.exists(directory):
            os.makedirs(directory)
        tile.save(os.path.join(directory, filename))
        filenames.append(filename)
    return filenames

