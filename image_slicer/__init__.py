# -*- coding: utf-8 -*-

"""Top-level package for Image Slicer."""

__author__ = "Sam Dobson"
__email__ = "1309834+samdobson@users.noreply.github.com"
# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "2.0.0"


def get_module_version():
    return __version__


from .main import *  # noqa: F401,F402,F403
from .helpers import *  # noqa: F401,F402,F403
