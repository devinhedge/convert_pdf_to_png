"""
test_pdf_converter.py - A command-line tool to convert PDFs into PNG images.

Author: Devin B. Hedge
Created: 03-Feb-2025
License: MIT License (see LICENSE file for details)

Copyright (c) 2025 Devin B. Hedge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import pytest
from pathlib import Path
from pdf_converter import convert_pdf_to_png, DEFAULT_OUTPUT_DIR

def test_pdf_conversion(tmp_path):
    """
    Test converting a multi-page PDF to PNG images.
    
    This test ensures that:
    1. The function correctly generates PNG images from the test PDF.
    2. The filenames match the expected naming format.
    3. The default output directory is used if no output directory is specified.
    """
    # Test PDF file (Ensure a sample test.pdf is placed in the tests directory)
    pdf_path = Path(__file__).parent / "test.pdf"

    # Ensure the test PDF exists
    if not pdf_path.exists():
        pytest.fail(f"Test PDF file '{pdf_path}' is missing. Please add a sample PDF for testing.")

    # Use the default output directory (./output)
    output_dir = DEFAULT_OUTPUT_DIR

    # Call the function without specifying an output directory
    convert_pdf_to_png(str(pdf_path), None, 150)

    # Get list of generated PNG files and ensure they are sorted correctly
    output_files = sorted(output_dir.glob("*.png"), key=lambda f: int(f.stem.split("_")[-1]))

    # Ensure at least one PNG file was created
    assert len(output_files) > 0, "No PNG files were generated."

    # Ensure filenames follow expected format
    for i, file in enumerate(output_files, start=1):
        expected_name = f"{pdf_path.stem}_page_{i}.png"
        assert file.name == expected_name, f"Expected filename {expected_name}, but got {file.name}"

def test_custom_output_directory(tmp_path):
    """
    Test conversion with a custom output directory.
    """
    pdf_path = Path(__file__).parent / "test.pdf"

    # Ensure the test PDF exists
    if not pdf_path.exists():
        pytest.fail(f"Test PDF file '{pdf_path}' is missing. Please add a sample PDF for testing.")

    # Custom output directory inside pytest's temp directory
    custom_output_dir = tmp_path / "custom_output"

    # Call the function with the custom output directory
    convert_pdf_to_png(str(pdf_path), str(custom_output_dir), 150)

    # Get list of generated PNG files and ensure they are sorted correctly
    output_files = sorted(custom_output_dir.glob("*.png"), key=lambda f: int(f.stem.split("_")[-1]))

    # Ensure at least one PNG file was created
    assert len(output_files) > 0, "No PNG files were generated in custom directory."

    # Ensure filenames follow expected format
    for i, file in enumerate(output_files, start=1):
        expected_name = f"{pdf_path.stem}_page_{i}.png"
        assert file.name == expected_name, f"Expected filename {expected_name}, but got {file.name}"
