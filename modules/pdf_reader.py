import fitz

def extract_text_from_pdf(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")

        text += f"\n\n--- Page {page_num} ---\n"
        text += page_text

    doc.close()

    return text.strip()