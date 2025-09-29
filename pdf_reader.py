import PyPDF2
import io

def read_pdf(file):
    """
    Reads the text content from an uploaded PDF file.
    Args:
        file: An uploaded file object from Streamlit.
    Returns:
        A string containing all the text from the PDF.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF file: {e}"