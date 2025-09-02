"""
Command-line interface for joining image tiles.
"""

import argparse

from .slicer import join_image


def main():
    """
    The main function for the image-joiner CLI.
    """
    parser = argparse.ArgumentParser(
        description="Join image tiles back into a single image.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("tiles_dir", help="Directory containing the tiles to join.")
    parser.add_argument(
        "output_path", help="Path where the joined image will be saved."
    )

    parser.add_argument(
        "-f",
        "--format",
        dest="naming_format",
        default="tile_{row}_{col}.png",
        help="A format string for the tile filenames. "
        "Available placeholders: {row}, {col}. "
        'Default: "tile_{row}_{col}.png"',
    )

    args = parser.parse_args()

    join_image(
        tiles_dir=args.tiles_dir,
        output_path=args.output_path,
        naming_format=args.naming_format,
    )


if __name__ == "__main__":
    main()
