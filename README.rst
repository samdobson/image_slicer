.. image:: https://badge.fury.io/py/image_slicer.png
    :target: http://badge.fury.io/py/image_slicer

.. image:: https://secure.travis-ci.org/samdobson/image_slicer.png
    :target: http://travis-ci.org/samdobson/image_slicer

.. image:: https://coveralls.io/repos/samdobson/image_slicer/badge.png
    :target: https://coveralls.io/r/samdobson/image_slicer

documentation_ | website_


Image Slicer
============

What does it do?
----------------

Splits an image into ``n`` equally-sized tiles. Also capable of joining the pieces back together.

Whether you are planning a collaborative art project, creating a jigsaw puzzle, or simply get a kick out of dividing images into identical quadrilaterals... this package is for you!

Installation
------------

.. code-block:: bash

	$ pip install image_slicer

*Python versions supported:*

* 2.6+
* 3.2+

Usage
-----

Slice an image with Python:

.. code-block:: python

	import image_slicer
	img = 'cake.jpg'
	num_tiles = 36
	tiles = image_slicer.split_image(img, num_tiles)
	image_slicer.save_tiles(tiles)

... or from the command line:

.. code-block:: bash

	$ slice-image cake.jpg 36

`Further examples`_ can be found in the documentation_.

About
-----

This module was developed for collabart_, a web application to help you launch a collaborative art project.

.. _Further examples: https://image-slicer.readthedocs.org/en/latest/examples/
.. _documentation: https://image-slicer.readthedocs.org/en/latest/
.. _website: http://samdobson.github.io/image_slicer
.. _collabart: http://www.collabart.com

