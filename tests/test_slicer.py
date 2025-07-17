import math
import os

import pytest
import pyvips

from image_slicer import ImageSlicer, slice_image
from image_slicer.slicer import _get_grid_from_tiles

TEST_IMAGE_WIDTH = 100
TEST_IMAGE_HEIGHT = 85


@pytest.fixture(scope="module")
def test_image_path(tmpdir_factory):
    """
    Creates a temporary black PNG image for testing.
    """
    path = str(tmpdir_factory.mktemp("data").join("test_image.png"))
    image = pyvips.Image.black(TEST_IMAGE_WIDTH, TEST_IMAGE_HEIGHT, bands=1)
    image.write_to_file(path)
    return path


def test_slice_by_columns_and_rows(test_image_path, tmp_path):
    """
    Tests slicing into a specific grid of columns and rows.
    """
    output_dir = str(tmp_path / "output_grid")
    cols, rows = 3, 2
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=output_dir, cols=cols, rows=rows)

    files = os.listdir(output_dir)
    assert len(files) == cols * rows  # 3*2 = 6 tiles

    # Check dimensions of a sample tile
    tile_w = math.ceil(TEST_IMAGE_WIDTH / cols)
    tile_h = math.ceil(TEST_IMAGE_HEIGHT / rows)
    a_tile = pyvips.Image.new_from_file(os.path.join(output_dir, "tile_0_0.png"))
    assert a_tile.width == tile_w
    assert a_tile.height == tile_h


def test_slice_by_number_of_tiles(test_image_path, tmp_path):
    """
    Tests slicing into a specific number of tiles.
    """
    output_dir = str(tmp_path / "output_num_tiles")
    num_tiles = 6  # Should result in a 2x3 grid
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=output_dir, number_of_tiles=num_tiles)

    files = os.listdir(output_dir)
    assert len(files) == num_tiles


def test_slice_by_tile_size(test_image_path, tmp_path):
    """
    Tests slicing by specifying tile width and height.
    """
    output_dir = str(tmp_path / "output_tile_size")
    tile_w, tile_h = 30, 25
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=output_dir, tile_width=tile_w, tile_height=tile_h)

    expected_cols = math.ceil(TEST_IMAGE_WIDTH / tile_w)
    expected_rows = math.ceil(TEST_IMAGE_HEIGHT / tile_h)
    files = os.listdir(output_dir)
    assert len(files) == expected_cols * expected_rows

    # Check a full-sized tile
    a_tile = pyvips.Image.new_from_file(os.path.join(output_dir, "tile_0_0.png"))
    assert a_tile.width == tile_w
    assert a_tile.height == tile_h

    # Check a right-edge partial tile
    last_col_tile = pyvips.Image.new_from_file(
        os.path.join(output_dir, f"tile_0_{expected_cols-1}.png")
    )
    expected_width = TEST_IMAGE_WIDTH % tile_w or tile_w
    assert last_col_tile.width == expected_width

    # Check a bottom-edge partial tile
    last_row_tile = pyvips.Image.new_from_file(
        os.path.join(output_dir, f"tile_{expected_rows-1}_0.png")
    )
    expected_height = TEST_IMAGE_HEIGHT % tile_h or tile_h
    assert last_row_tile.height == expected_height


def test_slice_with_prime_number_of_tiles_raises_error(test_image_path):
    """
    Tests that providing a prime number for tiles (which can't form a grid)
    raises a ValueError.
    """
    slicer = ImageSlicer(test_image_path)
    with pytest.raises(ValueError, match="Cannot form a grid with 5 tiles"):
        slicer.slice(output_dir="dummy", number_of_tiles=5)


def test_get_grid_from_tiles_logic():
    """
    Tests the internal logic for calculating grid dimensions from tile count.
    """
    assert _get_grid_from_tiles(4) == (2, 2)
    assert _get_grid_from_tiles(6) == (2, 3)
    assert _get_grid_from_tiles(8) == (2, 4)
    assert _get_grid_from_tiles(9) == (3, 3)
    assert _get_grid_from_tiles(12) == (3, 4)

    with pytest.raises(ValueError):
        _get_grid_from_tiles(0)
    with pytest.raises(ValueError):
        _get_grid_from_tiles(7)  # Prime number


def test_slice_without_criteria_raises_error(test_image_path):
    """
    Tests that calling slice without any slicing criteria raises an error.
    """
    slicer = ImageSlicer(test_image_path)
    with pytest.raises(ValueError, match="Slicing criteria not provided"):
        slicer.slice(output_dir="dummy")


def test_generate_tiles_by_grid(test_image_path):
    """
    Tests the generator with a specified grid.
    """
    slicer = ImageSlicer(test_image_path)
    cols, rows = 4, 3
    tiles = list(slicer.generate_tiles(cols=cols, rows=rows))

    assert len(tiles) == 12
    # Check metadata of the last tile
    last_tile, r, c = tiles[-1]
    assert r == rows - 1
    assert c == cols - 1
    assert isinstance(last_tile, pyvips.Image)


def test_generate_tiles_by_number(test_image_path):
    """
    Tests the generator with a specified number of tiles.
    """
    slicer = ImageSlicer(test_image_path)
    num_tiles = 9  # 3x3 grid
    tiles = list(slicer.generate_tiles(number_of_tiles=num_tiles))

    assert len(tiles) == num_tiles
    last_tile, r, c = tiles[-1]
    assert r == 2  # 3 rows
    assert c == 2  # 3 cols


def test_slice_image_convenience_function(test_image_path, tmp_path):
    """
    Tests the convenience `slice_image` function with new parameters.
    """
    output_dir = str(tmp_path / "output_convenience")
    num_tiles = 4
    slice_image(
        source_path=test_image_path, output_dir=output_dir, number_of_tiles=num_tiles
    )

    files = os.listdir(output_dir)
    assert len(files) == num_tiles


def test_partial_tiles_are_created_correctly(test_image_path, tmp_path):
    """
    Tests that partial tiles at the edges have the correct (smaller) dimensions.
    """
    output_dir = str(tmp_path / "output_partial")
    cols, rows = 3, 3
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=output_dir, cols=cols, rows=rows)

    # Expected tile sizes
    tile_w = math.ceil(TEST_IMAGE_WIDTH / cols)  # 100/3 = 34
    tile_h = math.ceil(TEST_IMAGE_HEIGHT / rows)  # 85/3 = 29

    # Check a full-sized tile
    tile_0_0 = pyvips.Image.new_from_file(os.path.join(output_dir, "tile_0_0.png"))
    assert tile_0_0.width == tile_w
    assert tile_0_0.height == tile_h

    # Check a right-edge partial tile
    # Expected width = 100 - (2 * 34) = 32
    tile_0_2 = pyvips.Image.new_from_file(os.path.join(output_dir, "tile_0_2.png"))
    assert tile_0_2.width == TEST_IMAGE_WIDTH - (2 * tile_w)
    assert tile_0_2.height == tile_h

    # Check a bottom-edge partial tile
    # Expected height = 85 - (2 * 29) = 27
    tile_2_0 = pyvips.Image.new_from_file(os.path.join(output_dir, "tile_2_0.png"))
    assert tile_2_0.width == tile_w
    assert tile_2_0.height == TEST_IMAGE_HEIGHT - (2 * tile_h)


def test_invalid_image_path_raises_error():
    """
    Tests that a pyvips.Error is raised for a non-existent or invalid image.
    """
    with pytest.raises(pyvips.Error):
        ImageSlicer("path/to/non_existent_image.png")


def test_naming_format(test_image_path, tmp_path):
    """
    Tests that the `naming_format` argument works correctly.
    """
    output_dir = str(tmp_path / "output_naming")
    naming_format = "slice_row{row}_col{col}.jpg"
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=output_dir, cols=2, rows=2, naming_format=naming_format)

    files = os.listdir(output_dir)
    assert "slice_row0_col0.jpg" in files
    assert "slice_row1_col1.jpg" in files
    assert len(files) == 4
