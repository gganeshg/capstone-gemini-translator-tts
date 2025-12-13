import io
import pandas as pd
from pypdf import PdfReader  # assuming you already moved to pypdf

class FileProcessor:
    @staticmethod
    def extract_text(file) -> str:
        mime = file.type.lower()

        if mime == "text/plain":
            return file.read().decode("utf-8", errors="ignore")

        if mime == "application/pdf":
            return FileProcessor._extract_pdf_text(file)

        if mime in (
            "text/csv",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ):
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
        # Reset pointer just in case
        file.seek(0)

        # Try CSV first (no header so we don't lose first row)
        try:
            df = pd.read_csv(file, header=None)
        except Exception:
            # Reset pointer again for Excel read
            file.seek(0)
            df = pd.read_excel(file, header=None)

        lines = []
        for _, row in df.iterrows():
            cells = [str(x) for x in row.tolist() if pd.notna(x)]
            if cells:
                lines.append(" ".join(cells))

        return "\n".join(lines)
