from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from logger import get_logger
from dotenv import load_dotenv
import os

logger = get_logger(__name__)
load_dotenv()

# embed the text and store in vector db
def store_chunk_in_chroma(chunks:list, persist_directory="chroma-db")-> Chroma:
    try:
        if not chunks:
            logger.warning("No chunks provided for embedding.")
            return None
        
        # open ai api key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Please check your .env file.")

        # embedding model
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)

        # store chunks in chromadb
        vector_db = Chroma.from_texts(
            texts = chunks,
            embedding = embeddings,
            persist_directory = persist_directory
        )

        logger.info(f"Stored {len(chunks)} chunks in ChromaDB at {persist_directory}.")
        return vector_db
    
    except Exception as e:
        logger.exception("Failed to embed and store chunks.")
        return None
