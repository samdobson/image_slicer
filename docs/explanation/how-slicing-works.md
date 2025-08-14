# How Slicing Works

This section provides a conceptual overview of the core logic behind `image-slicer`.

## The Core Engine: `pyvips`

`image-slicer` uses `pyvips`, a Python binding for the `libvips` image processing library. `libvips` is designed for performance and can process very large images without loading them entirely into memory. It works by streaming the image from disk, processing it in small chunks, and writing the output to disk. This is what allows `image-slicer` to be so fast and memory-efficient.

## Slicing Logic

When you request to slice an image, here's the process `image-slicer` follows:

1.  **Calculate Tile Dimensions**:
    -   If you provide `cols` and `rows`, the tile width and height are calculated by dividing the image dimensions by the number of columns and rows.
    -   If you provide `number_of_tiles`, the library finds all the factor pairs of that number (e.g., for 12, it finds `(1, 12)`, `(2, 6)`, `(3, 4)`, etc.). It then chooses the pair with the smallest difference (e.g., `(3, 4)`) to create a grid that is as close to a square as possible.

2.  **Handle Imperfect Divisions**:
    -   It's rare for an image's dimensions to be perfectly divisible by the number of tiles. For example, an 800-pixel wide image sliced into 3 columns would result in tiles that are 266.66 pixels wide.
    -   `image-slicer` handles this by using `math.ceil()` to round the tile dimension up to the nearest whole pixel (e.g., 267 pixels).
    -   When cropping the tiles, it ensures that the crop area never goes beyond the image boundaries. This means that tiles on the right and bottom edges might be slightly smaller than the other tiles. This is known as creating "partial" tiles.

3.  **Iterate and Crop**:
    -   The library iterates through the calculated grid, from top to bottom and left to right.
    -   For each position, it uses `pyvips` to crop a section of the source image corresponding to the tile's dimensions.
    -   The cropped tile is then saved to the specified output directory with the formatted filename.
