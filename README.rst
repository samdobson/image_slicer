.. image:: https://badge.fury.io/py/image_slicer.png
    :target: http://badge.fury.io/py/image_slicer

.. image:: https://secure.travis-ci.org/samdobson/image_slicer.png
    :target: http://travis-ci.org/samdobson/image_slicer

.. image:: https://coveralls.io/repos/samdobson/image_slicer/badge.png?branch=master
    :target: https://coveralls.io/r/samdobson/image_slicer?branch=master

Image Slicer
============

What does it do?
----------------

Splits an image into >n equally-sized tiles. Also capable of joining the pieces back together.

Whether you are planning a collaborative art project, creating a jigsaw puzzle, or simply enjoy dividing images into perfectly equal squares, this module is for you!

Installation
------------

::
	$ pip install image_slicer

Compatibility
-------------

* Python >=2.7
* Python >=3.2

Usage
-----

Slice an image with Python:

.. code-block:: python

	>>> from image_slicer import split_image, join_tiles
	>>> file = 'fish.jpg'
	>>> num_tiles = 36
	>>> tiles = split_image(file, num_tiles)
	>>> save_tiles(tiles)

... or from the command line:

::
	$ slice-image fish.jpg 36

`Further examples`_ can be found in the documentation_.

About
-----

This module was developed for collabart_, a web application to help you launch a collaborative art project.

.. _Further examples: https://docs.readthedocs.org/examples
.. _documentation: https://docs.readthedocs.org
.. _collabart: http://www.collabart.com

