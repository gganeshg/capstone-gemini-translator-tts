# tests/test_file_processor.py
import io
from utils.file_processor import FileProcessor

class FakeFile:
    def __init__(self, content: bytes, mime: str):
        self._content = content
        self.type = mime
    def read(self):
        return self._content
    def seek(self, x):
        pass

def test_extract_text_plain():
    content = b"hello world"
    f = FakeFile(content, "text/plain")
    text = FileProcessor.extract_text(f)
    assert "hello world" in text