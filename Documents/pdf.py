from pathlib import Path
import pymupdf
from PIL import Image
from Documents.model import Document
from Documents.ocr import extract_text, ask_ocr, looks_garbled
from Material.config import CONSOLE


def render_page(page, dpi: int) -> Image.Image:
    """ renders a PDF page as a PIL image """

    pixmap = page.get_pixmap(dpi = dpi)
    return Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)


def get_meaningful_images(page, min_area: float = 0.05):
    """ returns images large enough to potentially contain useful information """

    page_area = page.rect.width * page.rect.height
    meaningful = []

    if page_area <= 0: return meaningful

    for image in page.get_image_info():
        bbox = image["bbox"]

        area_ratio = ((bbox[2]-bbox[0]) * (bbox[3]-bbox[1])) / page_area
        if area_ratio >= min_area: meaningful.append(image)

    return meaningful


def import_pdf(path: Path, dpi: int, language: str) -> Document:
    """ imports a PDF and optionally uses OCR for image-only pages """

    text = []; pages = 0
    has_text = False; has_images = False; ocr_used = False

    try:
        with pymupdf.open(path) as pdf:
            pages = len(pdf); page_information = []

            for page in pdf:
                # checks each page inside the pdf
                import unicodedata
                page_text = unicodedata.normalize("NFC", page.get_text("text", sort=True)).strip()
                usable_text = page_text and not looks_garbled(page_text)

                images = get_meaningful_images(page)

                page_information.append((page, usable_text, images))

                if usable_text: has_text = True
                if images: has_images = True

            use_ocr = False
            has_ocr_candidates = any(images or not usable_text for _, _, images, usable_text in page_information)

            if has_ocr_candidates: use_ocr = ask_ocr(path, pages)

            for page, usable_text, images in page_information:
                if usable_text: text.append(usable_text)    # Normal selectable text

                if images and use_ocr:
                    image = render_page(page, dpi)

                    ocr_text = extract_text(image, language)

                    if ocr_text:
                        text.append(ocr_text)
                        ocr_used = True

    except Exception as e: return CONSOLE.print(f"[red]import_documents: Error: {e}[/red]")

    title = (path.stem.replace("_", " ").replace("-", " "))
    return Document(title, "\n\n".join(text), pages, has_text, has_images, ocr_used)