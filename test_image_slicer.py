import image_slicer
from PIL import Image

img = Image.open('./image_slicer/test/sample.jpg')

tiles = image_slicer.slice('./image_slicer/test/sample.jpg',col=5,row=5)

size = image_slicer.get_combined_size(tiles)

print(img.size)

print(size)