import io
import pandas as pd
# from PyPDF2 import PdfReader
from pypdf import PdfReader

class FileProcessor:
    @staticmethod
    def extract_text(file) -> str:
        """
        file: UploadedFile from Streamlit (has .type and .name)
        Returns: plain text.
        """
        mime = file.type.lower()

        if mime == "text/plain":
            return file.read().decode("utf-8", errors="ignore")

        if mime == "application/pdf":
            return FileProcessor._extract_pdf_text(file)

        if mime in ("text/csv", "application/vnd.ms-excel",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
            return FileProcessor._extract_table_text(file)

        raise ValueError(f"Unsupported file type: {mime}")

    @staticmethod
    def _extract_pdf_text(file) -> str:
        file_bytes = io.BytesIO(file.read())
        reader = PdfReader(file_bytes)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    @staticmethod
    def _extract_table_text(file) -> str:
        # Use pandas to read CSV/Excel; then join all cells into lines.
        try:
            df = pd.read_csv(file)
        except Exception:
            file.seek(0)
            df = pd.read_excel(file)

        lines = []
        for _, row in df.iterrows():
            # join all non-null cells with spaces
            cells = [str(x) for x in row.tolist() if pd.notna(x)]
            if cells:
                lines.append(" ".join(cells))
        return "\n".join(lines)