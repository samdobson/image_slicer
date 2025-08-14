"""
A high-performance Python library to slice images into tiles.
"""

__version__ = "3.0.1"

from .slicer import ImageSlicer, slice_image

__all__ = ["ImageSlicer", "slice_image"]
