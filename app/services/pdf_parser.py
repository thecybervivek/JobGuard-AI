import pdfplumber
from app.utils.exceptions import ResumeParserError

def extract_pdf_text(path):
    try:
        pages = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        text = "\n".join(pages).strip()
        if not text:
            raise ResumeParserError("NO_TEXT_FOUND", "No readable text was found in the PDF.")
        return text
    except ResumeParserError:
        raise
    except Exception as exc:
        raise ResumeParserError("CORRUPTED_PDF", "Unable to read the PDF file.") from exc
