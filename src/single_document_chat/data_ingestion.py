import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utlis.model_loader import ModelLoader

class SingleDocIngestor:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed to initilize the document ingestor",error=str(e))
            raise DocumentPortalException("Failed to initilize the document ingestor",sys)
        
    def ingest_files(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to ingest the files", error=str(e))
            raise DocumentPortalException("Failed to ingest the files", sys)
        
    def _create_retriever(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to create the retriever", error = str(e))
            raise DocumentPortalException("Failed to create the retriever", sys)