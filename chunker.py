from langchain.text_splitter import RecursiveCharacterTextSplitter
from logger import get_logger

logger = get_logger(__name__)

# split the text into chunks
def chunk_text(text: str, chunk_size=500, chunk_overlap=50) -> list:
    try:
        if not text.strip():
            logger.warning("Empty text provided for chunking.")
            return []
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""]
        )
        chunks = splitter.split_text(text)
        logger.info(f"Text successfully split into {len(chunks)} chunks.")
        return chunks

    except Exception as e:
        logger.exception("Failed to split text into chunks.")
        return []
