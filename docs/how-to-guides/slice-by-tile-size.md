# How to Slice an Image by Tile Size

Sometimes, you know the exact dimensions you want your tiles to be. For example, you might need 512x512 pixel tiles for a mapping application or a game. This guide shows you how to slice an image by specifying the exact width and height of each tile.

## Using the CLI

The `imslice` command-line tool makes this easy. Use the `-t` or `--tile-size` option, followed by the desired width and height in pixels.

### Example

Let's say you have a large satellite image (`satellite.jpg`) and you want to cut it into 256x256 pixel tiles.

```bash
imslice satellite.jpg output/tiles --tile-size 256 256
```

-   `satellite.jpg`: Your source image.
-   `output/tiles`: The directory where the tiles will be saved.
-   `--tile-size 256 256`: This tells `imslice` to create tiles that are 256 pixels wide and 256 pixels high.

If the source image dimensions are not perfectly divisible by the tile size, the tiles at the right and bottom edges will be smaller to account for the remainder.

## Using the Python API

You can achieve the same result in your Python code by passing the `tile_width` and `tile_height` parameters to the `slice_image` function or the `ImageSlicer.slice` method.

### Example

Here's how to slice the same image into 256x256 pixel tiles using a Python script:

```python
from image_slicer import slice_image

slice_image(
    source_path="satellite.jpg",
    output_dir="output/tiles",
    tile_width=256,
    tile_height=256
)
```

This gives you the flexibility to integrate tile-based slicing directly into your image processing workflows.
