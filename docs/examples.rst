Examples
--------

Split an image
~~~~~~~~~~~~~~

Save tiles to the same directory as the image using the original filename as a prefix:

.. code-block:: python
   :emphasize-lines: 2

	>>> import image_slicer
	>>> image_slicer.slice('cake.jpg', 4)
	(<Tile #1 - cake_01_01.png>, <Tile #2 - cake_01_02.png>, <Tile #3 - cake_02_01.png>, <Tile #4 - cake_02_02.png>)

Control tile saving
~~~~~~~~~~~~~~~~~~~

Need more control over saving? Pass ``save=False`` and then use :py:func:`~image_slicer.main.save_tiles`:

.. code-block:: python

	>>> import image_slicer
	>>> tiles = image_slicer.slice('cake.jpg', 4, save=False)
	>>> image_slicer.save_tiles(tiles, directory='~/cake_slices',\
		       		    prefix='slice', format='jpg')
	(<Tile #1 - slice_01_01.jpg>, <Tile #2 - slice_01_02.jpg>, <Tile #3 - slice_02_01.jpg>, <Tile #4 - slice_02_02.jpg>)

Processing tile images
~~~~~~~~~~~~~~~~~~~~~~

You can perform further processing of the images in between calling :py:func:`~image_slicer.main.slice` and py:func:`~image_slicer.main.save_tiles`. The PIL ``Image`` object can be accessed with ``Tile.image``. Let's overlay the tile number on each tile:

.. code-block:: python

	import image_slicer
	from PIL import ImageDraw, ImageFont


	tiles = image_slicer.slice('cake.jpg', 4, save=False)

	for tile in tiles:
   	    overlay = ImageDraw.Draw(tile.image)
    	    overlay.text((5, 5), str(tile.number), (255, 255, 255),
            	         ImageFont.load_default())

    	image_slicer.save_tiles(tiles)

Keep it in memory
~~~~~~~~~~~~~~~~~

If the tile image files are not the final product and performance is a concern, consider using :py:class:`BytesIO` to create file-like objects instead of saving each of the files to disk. Let's use the :ref:`zipfile <python:zipfile>` module to create a zip archive, ``'tiles.zip'``:

*Example courtesy of `slice-image.net`_*

.. code-block:: python

	import io
	import zipfile

	import image_slicer


	tiles = image_slicer.slice('cake.jpg', 4, save=False)

        with zipfile.ZipFile('tiles.zip', 'w') as zip:
            for tile in tiles:
		with io.BytesIO() as data:
		    tile.save(data)
		    zip.writestr(tile.generate_filename(path=False),
		    		 data.getvalue())

.. _slice-image.net: http://slice-image.net

