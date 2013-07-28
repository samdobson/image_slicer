'''
Helper functions for ``image_slicer``.
'''
import os


def get_basename(filename):
    """Strip path and extension. Return basename."""
    return os.path.splitext(os.path.basename(filename))[0]

def open_images(directory):
    """Open all images in a directory. Return tuple of Image instances."""
    return [Image.open(file) for file in os.listdir(directory)]

def get_columns_rows(filenames):
    """Derive number of columns and rows from filenames."""
    tiles = []
    for filename in filenames:
        row, column = os.path.splitext(filename)[0][-5:].split('_')
        tiles.append((int(row), int(column)))
    rows = [pos[0] for pos in tiles]; columns = [pos[1] for pos in tiles]
    num_rows = max(rows); num_columns = max(columns)
    return (num_columns, num_rows)

