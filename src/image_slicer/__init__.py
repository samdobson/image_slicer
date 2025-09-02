"""
A high-performance Python library to slice images into tiles.
"""

__version__ = "3.0.1"

from .slicer import ImageJoiner, ImageSlicer, join_image, slice_image

__all__ = ["ImageSlicer", "ImageJoiner", "slice_image", "join_image"]
