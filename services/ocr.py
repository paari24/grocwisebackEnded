import pdfplumber, pytesseract
from PIL import Image
import io

def extract_text_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    return text.strip() if text else None

def ocr_pdf(file):
    images = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            pil_image = page.to_image().original
            images.append(pytesseract.image_to_string(pil_image))
    return "\n".join(images)
