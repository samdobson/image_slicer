Image Slicer
============

Slice images into tiles and rejoin them. Compatible with **Python 2.6+, 3.2+**. Relies on Pillow_ for image manipulation.

.. toctree::
   :maxdepth: 2

   examples
   functions

Installation
------------

.. code-block:: bash

	$ pip install image_slicer

Run tests:

.. code-block:: bash

	$ python setup.py test

Command-line tools
------------------

Two CLI tools are provided: ``slice-image`` and ``join-image``. These will be added to your PATH and can thus be called from any directory.

``slice-image``
~~~~~~~~~~~~~~~

*Usage:*

.. code-block:: bash

	$ slice-image image num_tiles

Unless an output directory is specified with ``--dir`` or ``-d`` tiles will be saved in the same location as the image. The original filename will be used as a prefix unless overridden with ``--prefix`` or ``-p``.

``join-tiles``
~~~~~~~~~~~~~~

*Usage:*

.. code-block:: bash

	$ join-tiles tile

Any of the tile images can be used as an argument - the others will be discovered automatically. Unless an output directory is specified with ``--dir`` or ``-d`` the image will be saved in the same location as the tiles. The prefix of the tiles will be used to save the image unless this is overridden with ``--filename`` or ``-f``.

Methods
-------

.. automodule:: image_slicer.main
	:noindex:
	:members: split_image, join_tiles

See :doc:`all functions <functions>`.

Methodology
~~~~~~~~~~~

Images are always split into exactly equal parts, even if this means creating more than the requested number.

.. note:: In future versions this behaviour will be overridable.

Tile filenames are appended with a 2-digit representation of the tile's grid position (*e.g* ``image_03_02.jpg``).

Limitations
~~~~~~~~~~~

The maximum number of tiles that can be produced is **9800**. This is an arbitrary limit which ensures that row and column numbers can be conveniently represented by two digits. Increasing it would break :py:func:`~image_slicer.helpers.get_columns_rows` and consequently, :py:func:`~image_slicer.main.join_tiles`.

Development
-----------

Fork the repository_ on GitHub, commit your changes and send a pull request.

Troubleshooting
---------------

If the following doesn't help then open an issue_.

``IOError: decoder %s not available``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You are missing some of the libraries required for Pillow_. The `Pillow documentation`_ will be able to help you. Try starting with the `platform-specific instructions`_.

Dependencies
------------

Just one: Pillow_. It will be installed automatically by ``pip`` or ``python setup.py``.


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. _Pillow: https://pypi.python.org/pypi/Pillow
.. _`Pillow documentation`: https://github.com/python-imaging/Pillow
.. _repository: https://github.com/samdobson/image_slicer
.. _issue: https://github.com/samdobson/image_slicer/issues
.. _platform-specific instructions: https://github.com/python-imaging/Pillow/#platform-specific-instructions

