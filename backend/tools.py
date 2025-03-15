import duckduckgo_search
from bs4 import BeautifulSoup
import requests
import html2text
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract

def process_pdf(file_path: str) -> str:
    """Extract text from a PDF file with OCR fallback."""
    try:
        reader = PdfReader(file_path)
        if len(reader.pages) == 0:
            return "Error: The PDF is empty or has no readable pages."
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            # Fallback to OCR using pytesseract
            from pdf2image import convert_from_path
            images = convert_from_path(file_path)
            for image in images:
                text += pytesseract.image_to_string(image) + "\n"
            if not text.strip():
                return "Error: No text could be extracted from the PDF. It may be encrypted or unreadable even with OCR."
        return text[:1000] + "..." if len(text) > 1000 else text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

def duckduckgo_search(query: str) -> str:
    """Search the internet using DuckDuckGo and return formatted results."""
    results = duckduckgo_search.DDGS().text(query, max_results=3)
    formatted_results = "\n".join(
        f"- {result['title']}: {result['body']} (URL: {result['href']})" for result in results
    )
    return formatted_results

def browse_web(url: str) -> str:
    """Fetch and summarize content from a specific URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        h = html2text.HTML2Text()
        h.ignore_links = True
        plain_text = h.handle(text)
        summary = plain_text[:500] + "..." if len(plain_text) > 500 else plain_text
        return summary
    except Exception as e:
        return f"Error browsing URL: {str(e)}"

def process_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        if len(reader.pages) == 0:
            return "Error: The PDF is empty or has no readable pages."
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if not text.strip():
            return "Error: No text could be extracted from the PDF. It may be a scanned image or encrypted."
        return text[:1000] + "..." if len(text) > 1000 else text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"