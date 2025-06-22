from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from logger import get_logger
import os
from dotenv import load_dotenv

logger = get_logger(__name__)
load_dotenv()

def get_qa_chain(vectorstore):
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found.")

        
        llm = ChatOpenAI(
            openai_api_key=api_key,
            temperature=0.7,
            model="gpt-3.5-turbo"  # or "gpt-4" 
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(search_type="similarity", k=3),
            return_source_documents=True
        )

        logger.info("Q&A chain initialized successfully.")
        return qa_chain

    except Exception as e:
        logger.exception("Failed to initialize Q&A chain.")
        return None
