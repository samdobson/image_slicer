.. image:: https://badge.fury.io/py/image_slicer.png
    :target: http://badge.fury.io/py/image_slicer

.. image :: https://pypip.in/d/image_slicer/badge.png
    :target: https://crate.io/packages/image_slicer
    :alt: Downloads

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

	>>> import image_slicer
	>>> image_slicer.split_image('cake.jpg', 4)
	(<Tile #1 - cake_01_01.png>, <Tile #2 - cake_01_02.png>, <Tile #3 - cake_02_01.png>, <Tile #4 - cake_02_02.png>)


... or from the command line:

.. code-block:: bash

	$ slice-image cake.jpg 36

`Further examples`_ can be found in the documentation_.

Used by
-------

* splitimag.es_
* *collabart* (coming soon)

About
-----

This module was developed for *collabart*, a web application for launching collaborative art projects.

.. _splitimag.es: http://splitimag.es
.. _Further examples: https://image-slicer.readthedocs.org/en/latest/examples/
.. _documentation: https://image-slicer.readthedocs.org/en/latest/
.. _website: http://samdobson.github.io/image_slicer

