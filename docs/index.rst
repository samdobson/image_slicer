Image Slicer
============

Installation
------------

Latest stable release:

.. code-block:: bash

	$ pip install image_slicer

Development version:

.. code-block:: bash

	$ git clone https://github.com/samdobson/image_slicer.git
	% python setup.py

Compatibility
-------------

Tested with Python 2.7, 3.2, 3.3.

Dependencies
------------

Just one: Pillow_ (>=2.0.0). It will be installed automatically if you use one of the above methods.

.. toctree::
   :maxdepth: 2

Command-line tools
------------------

Two CLI tools are provided: ``slice-image`` and ``join-image``. These can be used from any directory.

slice-image
~~~~~~~~~~~

Usage:

.. code-block:: bash

	$ slice-image image num_tiles

Unless you specify an output directory with ``--dir`` or ``-d``, tiles will be saved in the same location as the image. The original filename will be used as a prefix unless this is overridden with ``--prefix`` or ``-p``.

join-tiles
~~~~~~~~~~

Usage:

.. code-block:: bash

	$ join-tiles tile

Any of the tile images can be used as an argument - the others will be discovered automatically. Unless an output directory is specified with ``--dir`` or ``-d`` the image will be saved in the same location as the tiles. The prefix of the tiles will be used to save the image unless this is overridden with ``--filename`` or ``-f``.


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. _Pillow: https://pypi.python.org/pypi/Pillow

