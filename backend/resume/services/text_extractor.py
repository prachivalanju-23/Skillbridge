import io
import fitz  # PyMuPDF
from docx import Document


def extract_text(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith('.pdf'):
        pdf = fitz.open(stream=data, filetype='pdf')
        return '\n'.join(page.get_text() for page in pdf)

    if name.endswith('.docx'):
        doc = Document(io.BytesIO(data))
        parts = [p.text for p in doc.paragraphs]
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    parts.append(cell.text)
        return '\n'.join(parts)

    raise ValueError('Only PDF and DOCX files are supported')