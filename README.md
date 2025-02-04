# Convert a PDF to a sequence of PNG files

This is a simple python script that takes a PDF and converts it to a sequence of PNG files that can be used for OCR. The script is useful for when a PDF is lockdown fairly tightly and can't be OCR easily.

### **Project Structure**
```
.
├── src
│   ├── pdf_converter.py  # Main script
│
├── tests
│   ├── test_pdf_converter.py  # Pytest file
│
├── requirements.txt
├── README.md
├── .gitignore
```

---

## **Virtual Environment & Dependencies**
From the **root directory**, run:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## **Running the Script from `src/`**
You'll now execute the script from the project root like this:

```bash
python src/pdf_converter.py -p my_document.pdf -o output_directory -d 300
```
or, if inside `src/`:

```bash
python pdf_converter.py -p ../my_document.pdf -o ../output_directory -d 300
```
---
## **Testing**

### What This Test Does:
- Adds src/ to sys.path to import pdf_converter.py properly.
- Checks if the test PDF exists before running (if missing, it fails the test).
- Uses pytest's tmp_path fixture to create a temporary directory for output images.
- Calls convert_pdf_to_png() to process the test PDF.
- Asserts that at least one PNG file is generated.
- Checks filename format (test.pdf_page_1.png, etc.).


## **Test Setup Instructions**

### **Add a Sample PDF for Testing**
Ensure you place a small test PDF file inside `tests/`:
```
tests/test.pdf  # A valid single-page PDF file
```
Alternatively, generate a sample PDF using Python:
```python
from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, "This is a test PDF", ln=True, align="C")
pdf.output("tests/test.pdf")
```

## **Running Tests**

You can run `pytest` from the **root** of the project.

```bash
pytest tests
```
or, to see detailed output:

```bash
pytest -v tests
```

---