"""
Command-line interface for image-slicer.
"""

import argparse

from .slicer import slice_image


def main():
    """
    The main function for the image-slicer CLI.
    """
    parser = argparse.ArgumentParser(
        description="Slice an image into smaller tiles.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("source_path", help="Path to the source image.")
    parser.add_argument("output_dir", help="Directory to save the tiles in.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        "--grid",
        type=int,
        nargs=2,
        metavar=("COLS", "ROWS"),
        help="The number of columns and rows to slice the image into.",
    )
    group.add_argument(
        "-n",
        "--number-of-tiles",
        type=int,
        help="The total number of tiles to create.",
    )
    group.add_argument(
        "-t",
        "--tile-size",
        type=int,
        nargs=2,
        metavar=("WIDTH", "HEIGHT"),
        help="The width and height of each tile.",
    )

    parser.add_argument(
        "-f",
        "--format",
        dest="naming_format",
        default="tile_{row}_{col}.png",
        help="A format string for the output filenames. "
        "Available placeholders: {row}, {col}. "
        'Default: "tile_{row}_{col}.png"',
    )

    args = parser.parse_args()

    cols, rows = (None, None)
    if args.grid:
        cols, rows = args.grid

    tile_width, tile_height = (None, None)
    if args.tile_size:
        tile_width, tile_height = args.tile_size

    slice_image(
        source_path=args.source_path,
        output_dir=args.output_dir,
        naming_format=args.naming_format,
        cols=cols,
        rows=rows,
        number_of_tiles=args.number_of_tiles,
        tile_width=tile_width,
        tile_height=tile_height,
    )

if __name__ == "__main__":
    main()
