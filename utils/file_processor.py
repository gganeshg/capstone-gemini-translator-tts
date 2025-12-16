# utils/file_processor.py
import io
import pandas as pd
from pypdf import PdfReader

class FileProcessor:
    @staticmethod
    def extract_text(file) -> str:
        try:
            mime = (file.type or "").lower()

            # Always reset pointer before reading
            try:
                file.seek(0)
            except Exception:
                pass

            if mime == "text/plain":
                data = file.read()
                if not data:
                    return ""
                return data.decode("utf-8", errors="ignore")

            if mime == "application/pdf":
                return FileProcessor._extract_pdf_text(file)

            if mime in (
                "text/csv",
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ):
                return FileProcessor._extract_table_text(file)

            # fallback based on filename extension (sometimes type is empty)
            name = (getattr(file, "name", "") or "").lower()
            if name.endswith(".txt"):
                data = file.read()
                return (data or b"").decode("utf-8", errors="ignore")

            raise ValueError(f"Unsupported file type: {mime} ({name})")
        except Exception:
            # Always return string even on failure
            return ""

    @staticmethod
    def _extract_pdf_text(file) -> str:
        try:
            file.seek(0)
        except Exception:
            pass
        file_bytes = io.BytesIO(file.read() or b"")
        reader = PdfReader(file_bytes)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    @staticmethod
    def _extract_table_text(file) -> str:
        try:
            file.seek(0)
        except Exception:
            pass

        try:
            df = pd.read_csv(file, header=None)
        except Exception:
            try:
                file.seek(0)
            except Exception:
                pass
            df = pd.read_excel(file, header=None)

        lines = []
        for _, row in df.iterrows():
            cells = [str(x) for x in row.tolist() if pd.notna(x)]
            if cells:
                lines.append(" ".join(cells))
        return "\n".join(lines)
