"""
Core image slicing logic.
"""

from __future__ import annotations

import io
import math
import os
import re
from pathlib import Path
from typing import Any, Generator

import pyvips  # type: ignore[import-untyped]

try:
    from PIL import Image as PILImage
except ImportError:
    PILImage = None  # type: ignore[assignment]


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
        source_path (Optional[str]): Path to the source image (if loaded from file).
        image (pyvips.Image): The pyvips Image object.
        width (int): The width of the source image.
        height (int): The height of the source image.
    """

    def __init__(self, source: str | Any):
        """
        Initializes the ImageSlicer.

        Args:
            source: Either a path to the image file or a PIL Image object.

        Raises:
            pyvips.error.Error: If the source is not a valid image.
            ValueError: If PIL Image is provided but Pillow is not installed.
        """
        if isinstance(source, str):
            self.source_path: str | None = source
            self.image = pyvips.Image.new_from_file(source, access="random")
        elif PILImage is not None and isinstance(source, PILImage.Image):
            self.source_path = None
            # Convert PIL Image to pyvips Image
            buffer = io.BytesIO()
            source.save(buffer, format="PNG")
            buffer.seek(0)
            self.image = pyvips.Image.new_from_buffer(
                buffer.getvalue(), "", access="random"
            )
        else:
            # Handle invalid types or PIL not available
            if PILImage is None:
                raise ValueError(
                    "source must be either a string path or a PIL Image object"
                )
            else:
                raise ValueError(
                    "source must be either a string path or a PIL Image object"
                )

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
        else:
            rows, cols = rows, cols

        if cols and rows:
            calculated_tile_width = math.ceil(self.width / cols)
            calculated_tile_height = math.ceil(self.height / rows)
            return calculated_tile_width, calculated_tile_height

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


class ImageJoiner:
    """
    A class to join image tiles back into a single image.

    Attributes:
        tiles_dir (str): Path to the directory containing tiles.
        naming_format (str): The naming format used for the tiles.
    """

    def __init__(self, tiles_dir: str, naming_format: str = "tile_{row}_{col}.png"):
        """
        Initialize the ImageJoiner.

        Args:
            tiles_dir: Directory containing the tiles to join.
            naming_format: The naming format used for the tiles.
        """
        self.tiles_dir = Path(tiles_dir)
        self.naming_format = naming_format

        if not self.tiles_dir.exists():
            raise ValueError(f"Tiles directory does not exist: {tiles_dir}")

    def _parse_naming_format(self) -> tuple[str, str]:
        """Parse the naming format to extract row and col placeholders."""
        # Convert format string to regex pattern
        pattern = self.naming_format
        pattern = pattern.replace("{row}", r"(\d+)")
        pattern = pattern.replace("{col}", r"(\d+)")
        pattern = "^" + pattern + "$"
        return pattern, self.naming_format

    def _discover_tiles(self) -> dict[tuple[int, int], Path]:
        """
        Discover all tiles in the directory and return a mapping of
        (row, col) to file path.
        """
        pattern, _ = self._parse_naming_format()
        tiles = {}

        for file_path in self.tiles_dir.iterdir():
            if file_path.is_file():
                match = re.match(pattern, file_path.name)
                if match:
                    row, col = int(match.group(1)), int(match.group(2))
                    tiles[(row, col)] = file_path

        if not tiles:
            raise ValueError(
                f"No tiles found in {self.tiles_dir} "
                f"matching format {self.naming_format}"
            )

        return tiles

    def _calculate_grid_dimensions(
        self, tiles: dict[tuple[int, int], Path]
    ) -> tuple[int, int]:
        """Calculate the number of rows and columns from discovered tiles."""
        rows = max(row for row, _ in tiles.keys()) + 1
        cols = max(col for _, col in tiles.keys()) + 1
        return rows, cols

    def _validate_tiles(
        self, tiles: dict[tuple[int, int], Path], rows: int, cols: int
    ) -> None:
        """Validate that all expected tiles are present."""
        missing_tiles = []
        for row in range(rows):
            for col in range(cols):
                if (row, col) not in tiles:
                    missing_tiles.append(f"tile at ({row}, {col})")

        if missing_tiles:
            raise ValueError(f"Missing tiles: {', '.join(missing_tiles)}")

    def join(self, output_path: str) -> None:
        """
        Join the tiles back into a single image.

        Args:
            output_path: Path where the joined image will be saved.
        """
        tiles = self._discover_tiles()
        rows, cols = self._calculate_grid_dimensions(tiles)
        self._validate_tiles(tiles, rows, cols)

        # Create rows of tiles without loading dimensions

        # Create rows of tiles
        tile_rows = []
        for row in range(rows):
            row_tiles = []
            for col in range(cols):
                tile_path = str(tiles[(row, col)])
                tile = pyvips.Image.new_from_file(tile_path)
                row_tiles.append(tile)

            # Join tiles horizontally to create a row
            row_image = row_tiles[0]
            for tile in row_tiles[1:]:
                row_image = row_image.join(tile, "horizontal")
            tile_rows.append(row_image)

        # Join rows vertically to create the final image
        final_image = tile_rows[0]
        for row_image in tile_rows[1:]:
            final_image = final_image.join(row_image, "vertical")

        # Save the final image
        final_image.write_to_file(output_path)


def slice_image(
    source: str | Any,
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
        source: Either a path to the image file or a PIL Image object.
        output_dir: The directory to save the tiles in.
        naming_format: A format string for the output filenames.
        cols: The number of columns to slice the image into.
        rows: The number of rows to slice the image into.
        number_of_tiles: The total number of tiles to create.
        tile_width: The desired width of each tile.
        tile_height: The desired height of each tile.
    """
    slicer = ImageSlicer(source)
    slicer.slice(
        output_dir=output_dir,
        naming_format=naming_format,
        cols=cols,
        rows=rows,
        number_of_tiles=number_of_tiles,
        tile_width=tile_width,
        tile_height=tile_height,
    )


def join_image(
    tiles_dir: str,
    output_path: str,
    naming_format: str = "tile_{row}_{col}.png",
) -> None:
    """
    A convenience function to join tiles back into a single image.

    Args:
        tiles_dir: Directory containing the tiles to join.
        output_path: Path where the joined image will be saved.
        naming_format: The naming format used for the tiles.
    """
    joiner = ImageJoiner(tiles_dir, naming_format)
    joiner.join(output_path)
