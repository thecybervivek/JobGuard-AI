def test_pdf_module_import():
    from app.services.pdf_parser import extract_pdf_text
    assert callable(extract_pdf_text)
