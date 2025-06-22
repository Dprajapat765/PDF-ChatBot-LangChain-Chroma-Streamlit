import fitz
from logger import get_logger

logger = get_logger(__name__) 

# extract text by passing a pdf file and get all text of pdf as string
def extract_text_from_pdf(pdf_file)-> str:
    try:
        text = ""

        document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        logger.info(f"PDF loaded successfully with {len(document)} pages.")

        for page_num, page in enumerate(document, start=1):
            page_text = page.get_text('text')
            if page_text.strip():
                text += page_text
            else:
                logger.warning(f"Page {page_num} is empty or could not be read.")
        
        document.close()

        if not text.strip():
            logger.warning("No text found in the PDF file")
        else:
            logger.info(f"Extracted {len(text)} characters of text from PDF.")
        
        return text

    except Exception as e:
        logger.exception("Failed to extract text from PDF")
        return "" 


