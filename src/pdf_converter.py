"""
pdf_converter.py - A command-line tool to convert PDFs into PNG images.

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

import argparse
import logging
import sys
from pathlib import Path
from pdf2image import convert_from_path
from PIL import UnidentifiedImageError
import subprocess  # Needed for handling Poppler dependency issues
from typing import Optional

# Configure Logging
LOG_FILE = Path(__file__).parent.parent / "pdf_to_png.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)

DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent / "output"  # Default output directory

def validate_pdf_path(pdf_path: Path) -> None:
    """Validates if the given PDF file path exists and is a valid file."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"Error: PDF file '{pdf_path}' does not exist.")
    if not pdf_path.is_file():
        raise ValueError(f"Error: '{pdf_path}' is not a valid file.")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Error: '{pdf_path}' is not a PDF file.")

def validate_output_dir(output_dir: Path) -> None:
    """Validates if the output directory exists or attempts to create it."""
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Error: Could not create output directory '{output_dir}'. {e}")

def validate_dpi(dpi: int) -> None:
    """Validates if DPI is a positive integer."""
    if dpi <= 0:
        raise ValueError("Error: DPI must be a positive integer.")

def convert_pdf_to_png(pdf_path: str, output_dir: Optional[str] = None, dpi: int = 200) -> None:
    """
    Converts a PDF into PNG images.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str, optional): Directory where PNG files will be saved. Defaults to './output'.
        dpi (int, optional): Resolution in DPI for PNG images. Default is 200.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the input arguments are invalid.
        RuntimeError: If Poppler is not installed.
        UnidentifiedImageError: If an image conversion error occurs.
    """
    try:
        pdf_file = Path(pdf_path)
        output_directory = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR  # Use default if None

        # Validate inputs
        validate_pdf_path(pdf_file)
        validate_output_dir(output_directory)
        validate_dpi(dpi)

        logging.info(f"Converting '{pdf_file.name}' to PNG images at {dpi} DPI...")
        logging.info(f"Saving images to: {output_directory}")

        # Convert PDF to images
        images = convert_from_path(str(pdf_file), dpi=dpi)

        for index, image in enumerate(images, start=1):
            output_filename = output_directory / f"{pdf_file.stem}_page_{index}.png"
            image.save(output_filename, "PNG")
            logging.info(f"Saved: {output_filename}")

        logging.info("PDF conversion completed successfully.")

    except FileNotFoundError as e:
        logging.error(e)
    except ValueError as e:
        logging.error(e)
    except subprocess.CalledProcessError as e:  # Handles Poppler missing errors
        logging.error("Error: Poppler is not installed or cannot be found. Install it to proceed.")
    except UnidentifiedImageError:
        logging.error(f"Error: Failed to convert PDF '{pdf_path}' to images.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def main() -> None:
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert a PDF into PNG images.")
    parser.add_argument("-p", "--pdf_path", required=True, help="Path to the input PDF file.")
    parser.add_argument("-o", "--output_dir", help=f"Directory where PNG files will be saved. Defaults to '{DEFAULT_OUTPUT_DIR}'.")
    parser.add_argument("-d", "--dpi", type=int, default=200, help="Resolution (DPI) for the PNG images. Default is 200.")

    args = parser.parse_args()

    try:
        convert_pdf_to_png(args.pdf_path, args.output_dir, args.dpi)
    except KeyboardInterrupt:
        logging.warning("Process interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()
