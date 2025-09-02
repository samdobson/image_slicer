import argparse
import os
from unittest.mock import patch, MagicMock

import pytest
import pyvips

from image_slicer.cli import main


@pytest.fixture(scope="module")
def test_image_path(tmpdir_factory):
    """
    Creates a temporary black PNG image for testing.
    """
    path = str(tmpdir_factory.mktemp("data").join("test_image.png"))
    image = pyvips.Image.black(100, 85, bands=1)
    image.write_to_file(path)
    return path


def test_main_with_grid_arguments(test_image_path, tmp_path):
    """
    Tests the CLI main function with grid arguments.
    """
    output_dir = str(tmp_path / "output_cli_grid")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '--grid', '2', '3']):
        main()
    
    files = os.listdir(output_dir)
    assert len(files) == 6  # 2*3 = 6 tiles


def test_main_with_number_of_tiles_argument(test_image_path, tmp_path):
    """
    Tests the CLI main function with number of tiles argument.
    """
    output_dir = str(tmp_path / "output_cli_tiles")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '--number-of-tiles', '4']):
        main()
    
    files = os.listdir(output_dir)
    assert len(files) == 4


def test_main_with_tile_size_arguments(test_image_path, tmp_path):
    """
    Tests the CLI main function with tile size arguments.
    """
    output_dir = str(tmp_path / "output_cli_size")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '--tile-size', '50', '40']):
        main()
    
    files = os.listdir(output_dir)
    # 100/50 = 2 cols, 85/40 = 3 rows (rounded up) = 2*3 = 6 tiles
    assert len(files) == 6


def test_main_with_custom_format(test_image_path, tmp_path):
    """
    Tests the CLI main function with custom naming format.
    """
    output_dir = str(tmp_path / "output_cli_format")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '--grid', '2', '2', 
                           '--format', 'custom_{row}_{col}.jpg']):
        main()
    
    files = os.listdir(output_dir)
    assert 'custom_0_0.jpg' in files
    assert 'custom_1_1.jpg' in files
    assert len(files) == 4


def test_main_with_short_arguments(test_image_path, tmp_path):
    """
    Tests the CLI main function with short argument forms.
    """
    output_dir = str(tmp_path / "output_cli_short")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '-g', '3', '2']):
        main()
    
    files = os.listdir(output_dir)
    assert len(files) == 6  # 3*2 = 6 tiles


def test_main_number_of_tiles_short_form(test_image_path, tmp_path):
    """
    Tests the CLI main function with short form of number-of-tiles.
    """
    output_dir = str(tmp_path / "output_cli_n")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '-n', '9']):
        main()
    
    files = os.listdir(output_dir)
    assert len(files) == 9


def test_main_tile_size_short_form(test_image_path, tmp_path):
    """
    Tests the CLI main function with short form of tile-size.
    """
    output_dir = str(tmp_path / "output_cli_t")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '-t', '25', '30']):
        main()
    
    files = os.listdir(output_dir)
    # 100/25 = 4 cols, 85/30 = 3 rows (rounded up) = 4*3 = 12 tiles
    assert len(files) == 12


def test_main_custom_format_short_form(test_image_path, tmp_path):
    """
    Tests the CLI main function with short form of format.
    """
    output_dir = str(tmp_path / "output_cli_f")
    
    with patch('sys.argv', ['imslice', test_image_path, output_dir, '-g', '2', '2', 
                           '-f', 'piece_{row}_{col}.png']):
        main()
    
    files = os.listdir(output_dir)
    assert 'piece_0_0.png' in files
    assert 'piece_1_1.png' in files


def test_main_missing_required_argument():
    """
    Tests that the CLI raises SystemExit when required mutually exclusive group is missing.
    """
    with patch('sys.argv', ['imslice', 'source.png', 'output_dir']):
        with pytest.raises(SystemExit):
            main()


def test_main_conflicting_arguments():
    """
    Tests that the CLI raises SystemExit when mutually exclusive arguments are provided.
    """
    with patch('sys.argv', ['imslice', 'source.png', 'output_dir', 
                           '--grid', '2', '2', '--number-of-tiles', '4']):
        with pytest.raises(SystemExit):
            main()


def test_main_invalid_image_path(tmp_path):
    """
    Tests that the CLI handles invalid image paths gracefully.
    """
    output_dir = str(tmp_path / "output_cli_invalid")
    
    with patch('sys.argv', ['imslice', 'nonexistent.png', output_dir, '--grid', '2', '2']):
        with pytest.raises(pyvips.Error):
            main()


def test_main_module_execution(test_image_path, tmp_path):
    """
    Tests the __main__ execution path of the CLI module.
    """
    import subprocess
    import sys
    
    output_dir = str(tmp_path / "output_main_module")
    
    # Execute the CLI module directly via Python
    result = subprocess.run([
        sys.executable, '-m', 'image_slicer.cli',
        test_image_path, output_dir, '--grid', '2', '2'
    ], cwd='/Users/sam/image_slicer', env={'PYTHONPATH': 'src'}, 
       capture_output=True, text=True)
    
    # Check that it executed successfully
    assert result.returncode == 0
    
    # Check that files were created
    files = os.listdir(output_dir)
    assert len(files) == 4  # 2*2 = 4 tiles