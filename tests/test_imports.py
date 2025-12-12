def test_imports():
    from utils.file_processor import FileProcessor
    from services.translator import TranslationService
    assert FileProcessor is not None
    assert TranslationService is not None
