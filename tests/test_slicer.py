import math
import os

import pytest
import pyvips

from image_slicer import ImageJoiner, ImageSlicer, join_image, slice_image
from image_slicer.slicer import _get_grid_from_tiles

try:
    from PIL import Image as PILImage

    PIL_AVAILABLE = True
except ImportError:
    PILImage = None  # type: ignore
    PIL_AVAILABLE = False

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
    # Test small numbers (edge cases)
    assert _get_grid_from_tiles(1) == (1, 1)
    assert _get_grid_from_tiles(2) == (1, 2)
    assert _get_grid_from_tiles(3) == (1, 3)

    # Test larger numbers
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
        source=test_image_path, output_dir=output_dir, number_of_tiles=num_tiles
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


def test_calculate_tile_dimensions_error_case(test_image_path):
    """
    Tests the error case in _calculate_tile_dimensions with insufficient params.
    """
    slicer = ImageSlicer(test_image_path)

    # This should raise an error since neither tile_width/height nor cols/rows
    # nor number_of_tiles are provided
    with pytest.raises(ValueError, match="You must specify either"):
        slicer._calculate_tile_dimensions()


def test_generate_tiles_without_criteria_raises_error(test_image_path):
    """
    Tests that calling generate_tiles without any slicing criteria raises an error.
    """
    slicer = ImageSlicer(test_image_path)

    # This should match the error on line 195
    with pytest.raises(ValueError, match="Slicing criteria not provided"):
        list(slicer.generate_tiles())


@pytest.mark.skipif(not PIL_AVAILABLE, reason="PIL/Pillow not available")
def test_pil_image_input(tmp_path):
    """
    Tests that the ImageSlicer can accept a PIL Image object as input.
    """
    # Create a PIL Image
    pil_image = PILImage.new("RGB", (TEST_IMAGE_WIDTH, TEST_IMAGE_HEIGHT), color="red")

    # Test with ImageSlicer
    slicer = ImageSlicer(pil_image)
    assert slicer.width == TEST_IMAGE_WIDTH
    assert slicer.height == TEST_IMAGE_HEIGHT
    assert slicer.source_path is None

    # Test slicing works
    output_dir = str(tmp_path / "output_pil")
    slicer.slice(output_dir=output_dir, cols=2, rows=2)

    files = os.listdir(output_dir)
    assert len(files) == 4


@pytest.mark.skipif(not PIL_AVAILABLE, reason="PIL/Pillow not available")
def test_slice_image_with_pil_input(tmp_path):
    """
    Tests that the slice_image convenience function works with PIL Image input.
    """
    pil_image = PILImage.new("RGB", (TEST_IMAGE_WIDTH, TEST_IMAGE_HEIGHT), color="blue")
    output_dir = str(tmp_path / "output_pil_convenience")

    slice_image(source=pil_image, output_dir=output_dir, number_of_tiles=4)

    files = os.listdir(output_dir)
    assert len(files) == 4


def test_invalid_source_type():
    """
    Tests that providing an invalid source type raises ValueError.
    """
    with pytest.raises(
        ValueError, match="source must be either a string path or a PIL Image object"
    ):
        ImageSlicer(123)  # Invalid type


def test_join_tiles_basic(test_image_path, tmp_path):
    """
    Tests basic tile joining functionality.
    """
    # First, slice the image
    tiles_dir = str(tmp_path / "tiles")
    output_path = str(tmp_path / "joined.png")

    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=tiles_dir, cols=2, rows=2)

    # Now join the tiles back together
    joiner = ImageJoiner(tiles_dir)
    joiner.join(output_path)

    # Verify the joined image exists and has correct dimensions
    assert os.path.exists(output_path)
    joined_image = pyvips.Image.new_from_file(output_path)
    assert joined_image.width == TEST_IMAGE_WIDTH
    assert joined_image.height == TEST_IMAGE_HEIGHT


def test_join_image_convenience_function(test_image_path, tmp_path):
    """
    Tests the join_image convenience function.
    """
    tiles_dir = str(tmp_path / "tiles")
    output_path = str(tmp_path / "joined.png")

    # Slice the image
    slice_image(test_image_path, tiles_dir, cols=3, rows=2)

    # Join using convenience function
    join_image(tiles_dir, output_path)

    # Verify the result
    assert os.path.exists(output_path)
    joined_image = pyvips.Image.new_from_file(output_path)
    assert joined_image.width == TEST_IMAGE_WIDTH
    assert joined_image.height == TEST_IMAGE_HEIGHT


def test_join_with_custom_naming_format(test_image_path, tmp_path):
    """
    Tests joining with a custom naming format.
    """
    tiles_dir = str(tmp_path / "tiles")
    output_path = str(tmp_path / "joined.png")
    naming_format = "slice_r{row}_c{col}.jpg"

    # Slice with custom naming format
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=tiles_dir, cols=2, rows=2, naming_format=naming_format)

    # Join with same naming format
    joiner = ImageJoiner(tiles_dir, naming_format)
    joiner.join(output_path)

    # Verify the result
    assert os.path.exists(output_path)
    joined_image = pyvips.Image.new_from_file(output_path)
    assert joined_image.width == TEST_IMAGE_WIDTH
    assert joined_image.height == TEST_IMAGE_HEIGHT


def test_join_tiles_nonexistent_directory():
    """
    Tests that ImageJoiner raises an error for non-existent directory.
    """
    with pytest.raises(ValueError, match="Tiles directory does not exist"):
        ImageJoiner("/path/to/nonexistent/directory")


def test_join_tiles_no_matching_tiles(tmp_path):
    """
    Tests that ImageJoiner raises an error when no matching tiles are found.
    """
    empty_dir = str(tmp_path / "empty")
    os.makedirs(empty_dir)

    joiner = ImageJoiner(empty_dir)
    with pytest.raises(ValueError, match="No tiles found"):
        joiner.join(str(tmp_path / "output.png"))


def test_join_tiles_missing_tiles(test_image_path, tmp_path):
    """
    Tests that ImageJoiner raises an error when some tiles are missing.
    """
    tiles_dir = str(tmp_path / "tiles")

    # Slice the image to create tiles
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=tiles_dir, cols=2, rows=2)

    # Remove one tile
    os.remove(os.path.join(tiles_dir, "tile_1_1.png"))

    # Try to join - should fail
    joiner = ImageJoiner(tiles_dir)
    with pytest.raises(ValueError, match="Missing tiles"):
        joiner.join(str(tmp_path / "output.png"))


def test_join_tiles_with_partial_edges(test_image_path, tmp_path):
    """
    Tests joining tiles that have partial edges (non-uniform tile sizes).
    """
    tiles_dir = str(tmp_path / "tiles")
    output_path = str(tmp_path / "joined.png")

    # Use a grid that creates partial tiles at edges
    slicer = ImageSlicer(test_image_path)
    slicer.slice(output_dir=tiles_dir, cols=3, rows=3)

    # Join the tiles
    joiner = ImageJoiner(tiles_dir)
    joiner.join(output_path)

    # Verify dimensions match original
    joined_image = pyvips.Image.new_from_file(output_path)
    assert joined_image.width == TEST_IMAGE_WIDTH
    assert joined_image.height == TEST_IMAGE_HEIGHT
