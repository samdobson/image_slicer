# API Reference

For more advanced use cases, you can use `image-slicer` directly from your Python code.

## `slice_image()`

This is the most straightforward way to use the slicer. It's a convenience function that handles everything for you.

```python
from image_slicer import slice_image

slice_image(
    source_path="path/to/image.jpg",
    output_dir="path/to/output",
    number_of_tiles=12
)
```

### Parameters

-   **`source_path`** (str): The path to the image file.
-   **`output_dir`** (str): The directory to save the tiles in.
-   **`naming_format`** (str, optional): A format string for the output filenames. Defaults to `"tile_{row}_{col}.png"`.
-   **`cols`** (int, optional): The number of columns to slice the image into.
-   **`rows`** (int, optional): The number of rows to slice the image into.
-   **`number_of_tiles`** (int, optional): The total number of tiles to create.
-   **`tile_width`** (int, optional): The width of each tile in pixels.
-   **`tile_height`** (int, optional): The height of each tile in pixels.

## `ImageSlicer` Class

If you need more control, you can use the `ImageSlicer` class. This is especially useful if you want to work with the tiles in memory before saving them.

```python
from image_slicer import ImageSlicer

slicer = ImageSlicer("path/to/image.jpg")
```

### `ImageSlicer.__init__(source_path)`

-   **`source_path`** (str): The path to the image file.

### `ImageSlicer.slice(...)`

Slices the image and saves the tiles to disk. The parameters are the same as the `slice_image()` function, excluding `source_path`.

```python
slicer.slice(
    output_dir="path/to/output",
    cols=4,
    rows=3
)
```

### `ImageSlicer.generate_tiles(...)`

A generator that yields tiles as `pyvips.Image` objects, along with their row and column numbers. This is useful for in-memory processing.

```python
for tile, row, col in slicer.generate_tiles(number_of_tiles=9):
    print(f"Processing tile at row {row}, col {col}")
    # ... do something with the 'tile' object ...
    tile.write_to_file(f"tile_{row}_{col}.png")
```
