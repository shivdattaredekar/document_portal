from __future__ import annotations # to get away with circular imports and future referencing
import os
import sys
import json
import uuid
import hashlib
import shutil
import fitz #type:ignore
from pathlib import Path
from datetime import datetime, timezone
from typing import (
    List,
    Dict,
    Any,
    Union,
    Optional,
    Tuple,
    Set,
    Callable,
    Iterable,
    TypeVar,
    Generic,
    Sequence,
    Mapping,
    MutableMapping,
    MutableSequence,
)

from langchain_community.document_loaders import (PyPDFLoader, #type:ignore
                                                PyPDFDirectoryLoader,
                                                Docx2txtLoader,
                                                TextLoader)

from langchain.text_splitter import RecursiveCharacterTextSplitter #type:ignore
from langchain_community.vectorstores import FAISS #type:ignore
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utlis.model_loader import ModelLoader


from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class FaissManager:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error(f"Failed to initialize the Faiss manager", error = str(e))
            raise DocumentPortalException(f"Error initializing the Faiss manager",sys)

    def _exists(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to check if the Faiss index exists", error = str(e))
            raise DocumentPortalException(f"Error checking if the Faiss index exists", sys)

    @staticmethod    
    def _fingerprint(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to generate the fingerprint", error = str(e))
            raise DocumentPortalException(f"Error generating the fingerprint", sys)

    def _save_metadata(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to save the metadata", error = str(e))
            raise DocumentPortalException(f"Error saving the metadata", sys)
        
    def add_documents(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to add documents to the Faiss index", error = str(e))
            raise DocumentPortalException(f"Error adding documents to the Faiss index", sys)
        
    def load_or_create(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to load or create the Faiss index", error = str(e))
            raise DocumentPortalException(f"Error loading or creating the Faiss index", sys)



class DocHandler:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as Ex:
            self.log.error(f"Failed to initialize the DocHandler", error = str(Ex))
            raise DocumentPortalException(f"Error in initializing the DocHandler",sys) 
        
    def save_pdf(self):
        try:
            pass
        except Exception as Ex:
            self.log.error(f"Failed to save the PDF", error = str(Ex))
            raise DocumentPortalException(f"Error in saving the PDF", sys)
    
    def read_pdf(self):
        try:
            pass
        except Exception as Ex:
            self.log.error(f"Failed to read the PDF", error = str(Ex))
            raise DocumentPortalException(f"Error in reading the PDF", sys)

class DocumentComparator:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as Ex:
            self.log.error(f"Failed to initialize the DocumentComparator", error = str(Ex))
            raise DocumentPortalException(f"Error in initializing the DocumentComparator", sys)
        
    def save_uploaded_files(self):
        try:
            pass
        except Exception as Ex:
            self.log.error(f"Failed to save the uploaded file", error = str(Ex))
            raise DocumentPortalException(f"Error in saving the uploaded file", sys)

    def read_pdf(self):
        try:
            pass
        except Exception as Ex:
            self.log.error(f"Failed to read the PDF", error = str(Ex))
            raise DocumentPortalException(f"Error in reading the PDF", sys)

    def combine_documents(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to combine the documents", error = str(e))
            raise DocumentPortalException(f"Error in combining the documents's", sys)


    def clean_old_sessions(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to clean the old sessions", error = str(e))
            raise DocumentPortalException(f"Error in cleaning the old sessions", sys)
        

class ChatIngestor:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as Ex:
            self.log.error(f"Failed to initialize the ChatIngestor", error = str(Ex))
            raise DocumentPortalException(f"Error in initializing the ChatIngestor", sys)
        
    def _resolve_dir(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to resolve the directory", error = str(e))
            raise DocumentPortalException(f"Error in resolving the directory", sys)
        
    def _split(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to split the documents", error = str(e))
            raise DocumentPortalException(f"Error in splitting the documents", sys)
    
    def buit_retriever(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Failed to build the retriever", error = str(e))
            raise DocumentPortalException(f"Error in building the retriever", sys)
        
        