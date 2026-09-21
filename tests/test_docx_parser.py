def test_docx_module_import():
    from app.services.docx_parser import extract_docx_text
    assert callable(extract_docx_text)
