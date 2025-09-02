# Image Slicer

[![Downloads](https://pepy.tech/badge/image-slicer)](https://pepy.tech/project/image-slicer)
[![PyPI version](https://badge.fury.io/py/image-slicer.svg)](https://badge.fury.io/py/image-slicer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage Status](https://coveralls.io/repos/github/samdobson/image_slicer/badge.svg?branch=master)](https://coveralls.io/github/samdobson/image_slicer?branch=master)

A high-performance Python library to slice images into tiles.

`image-slicer` provides a flexible and intuitive API to slice large images into smaller, manageable tiles. It uses `pyvips` as its backend, which makes it extremely fast and memory-efficient (up to 5x faster and 10x more memory-efficient than other approaches). It can process images far larger than your available system RAM.

## Features

- **High Performance**: Leverages the speed of `libvips`.
- **Memory Efficient**: Low memory usage, ideal for very large images.
- **Simple API**: Slice images with a single function call or use the `ImageSlicer` class for more control.
- **Flexible**: Customise tile sizes and output naming conventions.
- **Generator Support**: Process tiles in-memory without writing them all to disk.
- **Handles Any Image Size**: Automatically manages images that are not perfectly divisible by the tile size.

## Installation

You can use any modern Python package manager, such as `pip` or `uv`.

```bash
# Using uv
uv add image-slicer

# Or using pip
pip install image-slicer
```

## CLI Usage

`image-slicer` comes with a command-line interface (CLI) for easy use in scripts or for quick slicing tasks.

### Slice by Number of Tiles

This will slice the image into a specific number of tiles, automatically calculating the grid layout to be as square as possible.

```bash
imslice my_large_image.tif output_tiles --number-of-tiles 16
```

### Slice by Grid Dimensions

You can also specify the exact grid dimensions (columns and rows).

```bash
imslice my_large_image.tif output_tiles --grid 4 4
```

### Custom Naming Format

You can customise the output filenames using the `--format` option.

```bash
imslice my_large_image.tif output_tiles --grid 4 4 --format "tile_{row}_{col}.webp"
```

## Usage

You can use the simple `slice_image` function for a quick one-off task or the `ImageSlicer` class for more advanced use cases.

### Basic Example

This is the easiest way to get started. It will slice the image and save the tiles to the specified directory.

```python
from image_slicer import slice_image

# Slice a large image into 256x256 pixel tiles
slice_image(
    source_path="my_large_image.tif",
    output_dir="output_tiles",
    tile_width=256,
    tile_height=256,
)

print("Slicing complete!")
```

### Advanced Usage (Class-based)

For more control, instantiate the `ImageSlicer` class. This is useful if you want to inspect image properties before slicing or use the tile generator.

```python
from image_slicer import ImageSlicer

# Initialise the slicer
slicer = ImageSlicer("my_large_image.jpg")

print(f"Image dimensions: {slicer.width}x{slicer.height}")

# Slice the image with a custom naming format
slicer.slice(
    output_dir="output_tiles_custom",
    tile_width=512,
    tile_height=512,
    naming_format="slice_row-{row}_col-{col}.webp"
)
```

### In-Memory Tile Generation

If you need to process tiles without saving them to disk, you can use the `generate_tiles` method. It returns a generator that yields each tile as a `pyvips.Image` object.

```python
from image_slicer import ImageSlicer

slicer = ImageSlicer("another_image.png")

# Generate 100x100 pixel tiles
tile_generator = slicer.generate_tiles(tile_width=100, tile_height=100)

for tile, row, col in tile_generator:
    # ---
    # Process the 'tile' object here.
    # For example, you could convert it to a NumPy array,
    # run analysis, or stream it somewhere.
    # ---
    print(f"Processing tile ({row}, {col}) with size {tile.width}x{tile.height}")
    
    # Example: save only the first column of tiles
    if col == 0:
        tile.write_to_file(f"tile_col0_{row}.jpg")

```
