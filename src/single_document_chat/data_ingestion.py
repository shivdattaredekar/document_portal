import uuid
from pathlib import Path
import sys
from datetime import datetime, timezone
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utlis.model_loader import ModelLoader

class SingleDocIngestor:
    def __init__(self, data_dir:str = "data/single_document_chat", faiss_dir:str="faiss_index"):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)

            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            self.model_loader = ModelLoader()
            self.log.info("Single document ingestor initialized successfully", dir_path = str(self.data_dir),
                        faiss_dir = str(self.faiss_dir))
            
            
        except Exception as e:
            self.log.error("Failed to initilize the document ingestor",error=str(e))
            raise DocumentPortalException("Failed to initilize the document ingestor",sys)
        
    def ingest_files(self, uploaded_files):
        try:
            documents = []
            for uploaded_file in uploaded_files:
                unique_filename = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.pdf"

                temp_path = self.data_dir / unique_filename
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                self.log.info("Saved the file successfully", file_name=unique_filename)
            
                loader = PyPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs)
            self.log.info("Loaded the documents successfully", count=len(documents))
            return self._create_retriever(documents)

        except Exception as e:
            self.log.error("Failed to ingest the files", error=str(e))
            raise DocumentPortalException("Failed to ingest the files", sys)
        
    def _create_retriever(self, documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            texts = splitter.split_documents(documents)
            self.log.info("Split the documents successfully", count=len(texts))

            vectorstore = FAISS.from_documents(texts, self.model_loader.load_embeddings())
            self.log.info("Created the vector store successfully")

            # Save the vector store
            vectorstore.save_local(str(self.faiss_dir))
            self.log.info("Saved the vector store successfully", faiss_path=str(self.faiss_dir))

            retriever = vectorstore.as_retriever(search_type = "similarity",search_kwargs={"k": 5})
            self.log.info("Created the retriever successfully", retriever_type=str(type(retriever)))
            return retriever

        except Exception as e:
            self.log.error("Failed to create the retriever", error = str(e))
            raise DocumentPortalException("Failed to create the retriever", sys)