# Command-Line Interface (CLI) Reference

The `imslice` command provides a simple interface for slicing images.

## Usage

```bash
imslice [OPTIONS] <source_path> <output_dir>
```

## Positional Arguments

-   **`source_path`** (required)
    -   The path to the source image you want to slice.
    -   Example: `images/my_photo.jpg`

-   **`output_dir`** (required)
    -   The directory where the sliced tiles will be saved.
    -   If the directory does not exist, it will be created automatically.
    -   Example: `output/tiles`

## Slicing Options

You must provide one of the following mutually exclusive options to determine how the image will be sliced.

-   **`-n, --number-of-tiles <INTEGER>`**
    -   Specifies the total number of tiles to create.
    -   `image-slicer` will automatically calculate the grid layout (columns and rows) that is closest to a square.
    -   The number must be a positive integer with factors other than 1 and itself (e.g., 4, 6, 8, 9, 10, 12...).
    -   Example: `imslice ... --number-of-tiles 16` (creates a 4x4 grid)

-   **`-g, --grid <COLS> <ROWS>`**
    -   Specifies the exact grid layout in columns and rows.
    -   Provide two integers: the number of columns followed by the number of rows.
    -   Example: `imslice ... --grid 3 2` (creates a 3-column, 2-row grid)

-   **`-t, --tile-size <WIDTH> <HEIGHT>`**
    -   Specifies the exact dimensions of each tile in pixels.
    -   Provide two integers: the width followed by the height.
    -   Note: Tiles at the right and bottom edges may be smaller if the image dimensions are not perfectly divisible by the tile size.
    -   Example: `imslice ... --tile-size 512 512`

## Other Options

-   **`-f, --format <FORMAT_STRING>`**
    -   A format string for the output filenames.
    -   **Default**: `"tile_{row}_{col}.png"`
    -   **Available placeholders**:
        -   `{row}`: The row number of the tile (0-indexed).
        -   `{col}`: The column number of the tile (0-indexed).
    -   Example: `imslice ... --format "slice_y{row}_x{col}.jpg"`
