# How to Save Tiles to a Different Directory

By default, you specify the output directory when you run the `imslice` command. This guide shows you how to direct the output to any directory you choose.

## The `output_dir` Argument

The `imslice` command requires two positional arguments:

1.  `source_path`: The image you want to slice.
2.  `output_dir`: The directory where the tiles will be saved.

## Example

Let's say you have an image at `/path/to/my/image.jpg` and you want to save the tiles to a new directory called `my-sliced-images` on your Desktop.

Here's the command you would use:

```bash
# The output directory doesn't need to exist yet.
imslice /path/to/my/image.jpg ~/Desktop/my-sliced-images --grid 2 2
```

After the command finishes, the `~/Desktop/my-sliced-images` directory will be created, and it will contain the four sliced tiles.
