# Image Slicer

[![Downloads](https://pepy.tech/badge/image-slicer)](https://pepy.tech/project/image-slicer)
[![Build Status](https://github.com/samdobson/image_slicer/workflows/Build%20Master/badge.svg)](https://github.com/samdobson/image_slicer/actions)
[![Documentation](https://github.com/samdobson/image_slicer/workflows/Documentation/badge.svg)](https://samdobson.github.io/image_slicer)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code Coverage](https://codecov.io/gh/samdobson/image_slicer/branch/master/graph/badge.svg)](https://codecov.io/gh/samdobson/image_slicer)

Splitting images into tiles. With Python. Since 2013.

---

## Installation
**Latest Stable Release:** `pip install image_slicer`<br>
**Current Development Head:** `pip install git+https://github.com/samdobson/image_slicer.git`

## Quick Start

Slice your images either with the command line utility:

```bash
$ slice-image cake.png -n 4
```

... or from your Python script:

```python
from image_slicer import slice

slice('cake.png', 4)
```

## Documentation
For full package documentation please visit [samdobson.github.io/image_slicer](https://samdobson.github.io/image_slicer).

## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

