"""
Core image slicing logic.
"""

from __future__ import annotations

import math
import os
from typing import Generator

import pyvips


def _find_factors(n: int) -> list[tuple[int, int]]:
    """Finds all factor pairs of an integer."""
    factors = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add((i, n // i))
            factors.add((n // i, i))
    return sorted(factors, key=lambda x: x[0])


def _get_grid_from_tiles(
    num_tiles: int,
) -> tuple[int, int]:
    """
    Calculates the number of rows and columns for a given number of tiles.
    Tries to create a grid that is as close to a square as possible.
    """
    if num_tiles <= 0:
        raise ValueError("Number of tiles must be a positive integer.")

    if num_tiles == 1:
        return 1, 1
    if num_tiles == 2:
        return 1, 2
    if num_tiles == 3:
        return 1, 3

    factors = _find_factors(num_tiles)
    if not factors or (len(factors) == 2 and factors[0][0] == 1):
        raise ValueError(
            f"Cannot form a grid with {num_tiles} tiles. "
            "Please choose a number with more factors."
        )

    # Find the factor pair with the smallest difference (closest to a square)
    best_pair = min(factors, key=lambda p: abs(p[0] - p[1]))
    return best_pair


class ImageSlicer:
    """
    A class to slice a large image into smaller tiles.

    Uses pyvips for memory-efficient processing, allowing it to handle
    images that are much larger than the available RAM.

    Attributes:
        source_path (str): Path to the source image.
        image (pyvips.Image): The pyvips Image object.
        width (int): The width of the source image.
        height (int): The height of the source image.
    """

    def __init__(self, source_path: str):
        """
        Initializes the ImageSlicer.

        Args:
            source_path: The path to the image file to be sliced.

        Raises:
            pyvips.error.Error: If the source_path is not a valid image.
        """
        self.source_path = source_path
        self.image = pyvips.Image.new_from_file(source_path, access="random")
        self.width = self.image.width
        self.height = self.image.height

    def _calculate_tile_dimensions(
        self,
        cols: int | None = None,
        rows: int | None = None,
        number_of_tiles: int | None = None,
        tile_width: int | None = None,
        tile_height: int | None = None,
    ) -> tuple[int, int]:
        """
        Calculates the width and height of a single tile based on the
        specified number of columns, rows, or total number of tiles.
        """
        if tile_width and tile_height:
            return tile_width, tile_height

        if number_of_tiles:
            rows, cols = _get_grid_from_tiles(number_of_tiles)

        if cols and rows:
            tile_width = math.ceil(self.width / cols)
            tile_height = math.ceil(self.height / rows)
            return tile_width, tile_height

        raise ValueError(
            "You must specify either 'number_of_tiles', 'cols' and 'rows', "
            "or 'tile_width' and 'tile_height'."
        )

    def slice(
        self,
        output_dir: str,
        naming_format: str = "tile_{row}_{col}.png",
        cols: int | None = None,
        rows: int | None = None,
        number_of_tiles: int | None = None,
        tile_width: int | None = None,
        tile_height: int | None = None,
    ) -> None:
        """
        Slices the image into tiles and saves them to a directory.

        This method allows slicing based on a grid layout (cols, rows) or a
        target number of tiles.

        Note:
            If the image dimensions are not perfectly divisible, tiles at the
            right and bottom edges will be smaller ("partial" tiles).

        Args:
            output_dir: The directory to save the tiles in.
            naming_format: A format string for the output filenames.
                           Available placeholders: {row}, {col}.
            cols: The number of columns to slice the image into.
            rows: The number of rows to slice the image into.
            number_of_tiles: The total number of tiles to create. This will
                             override cols and rows.
            tile_width: The desired width of each tile.
            tile_height: The desired height of each tile.
        """
        if not any([cols, rows, number_of_tiles, tile_width, tile_height]):
            raise ValueError(
                "Slicing criteria not provided. Please specify 'cols' and "
                "'rows', 'number_of_tiles', or 'tile_width' and 'tile_height'."
            )

        tile_width, tile_height = self._calculate_tile_dimensions(
            cols, rows, number_of_tiles, tile_width, tile_height
        )

        os.makedirs(output_dir, exist_ok=True)
        for r in range(0, self.height, tile_height):
            for c in range(0, self.width, tile_width):
                left = c
                top = r
                width = min(tile_width, self.width - c)
                height = min(tile_height, self.height - r)

                tile = self.image.crop(left, top, width, height)

                row_num = r // tile_height
                col_num = c // tile_width

                filename = naming_format.format(row=row_num, col=col_num)
                output_path = os.path.join(output_dir, filename)

                tile.write_to_file(output_path)

    def generate_tiles(
        self,
        cols: int | None = None,
        rows: int | None = None,
        number_of_tiles: int | None = None,
        tile_width: int | None = None,
        tile_height: int | None = None,
    ) -> Generator[tuple[pyvips.Image, int, int], None, None]:
        """
        A generator that yields image tiles as pyvips.Image objects.

        Useful for processing tiles in memory without saving them to disk.

        Args:
            cols: The number of columns to slice the image into.
            rows: The number of rows to slice the image into.
            number_of_tiles: The total number of tiles to create. This will
                             override cols and rows.
            tile_width: The desired width of each tile.
            tile_height: The desired height of each tile.

        Yields:
            A tuple containing the pyvips.Image object for the tile,
            its row number, and its column number.
        """
        if not any([cols, rows, number_of_tiles, tile_width, tile_height]):
            raise ValueError(
                "Slicing criteria not provided. Please specify 'cols' and "
                "'rows', 'number_of_tiles', or 'tile_width' and 'tile_height'."
            )

        tile_width, tile_height = self._calculate_tile_dimensions(
            cols, rows, number_of_tiles, tile_width, tile_height
        )

        for r in range(0, self.height, tile_height):
            for c in range(0, self.width, tile_width):
                left = c
                top = r
                width = min(tile_width, self.width - c)
                height = min(tile_height, self.height - r)

                tile = self.image.crop(left, top, width, height)
                row_num = r // tile_height
                col_num = c // tile_width

                yield tile, row_num, col_num


def slice_image(
    source_path: str,
    output_dir: str,
    naming_format: str = "tile_{row}_{col}.png",
    cols: int | None = None,
    rows: int | None = None,
    number_of_tiles: int | None = None,
    tile_width: int | None = None,
    tile_height: int | None = None,
) -> None:
    """
    A convenience function to slice an image and save the tiles.

    Args:
        source_path: The path to the image file.
        output_dir: The directory to save the tiles in.
        naming_format: A format string for the output filenames.
        cols: The number of columns to slice the image into.
        rows: The number of rows to slice the image into.
        number_of_tiles: The total number of tiles to create.
        tile_width: The desired width of each tile.
        tile_height: The desired height of each tile.
    """
    slicer = ImageSlicer(source_path)
    slicer.slice(
        output_dir=output_dir,
        naming_format=naming_format,
        cols=cols,
        rows=rows,
        number_of_tiles=number_of_tiles,
        tile_width=tile_width,
        tile_height=tile_height,
    )
