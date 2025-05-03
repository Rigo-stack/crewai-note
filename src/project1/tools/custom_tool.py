from crewai_tools import tool
from docx import Document
import PyPDF2

# @tool
# def read_docx(file_path: str) -> str:
#     """Reads a .docx file and returns its full text."""
#     doc = Document(file_path)
#     return "\n".join([para.text for para in doc.paragraphs])

# @tool
# def read_pdf(file_path: str) -> str:
#     """Reads a .pdf file and returns its full text."""
#     text = ""
#     with open(file_path, "rb") as f:
#         reader = PyPDF2.PdfReader(f)
#         for page in reader.pages:
#             text += page.extract_text()
#     return text