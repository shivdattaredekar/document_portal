import os
import sys
import uuid
from pathlib import Path
from datetime import datetime, timezone
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader #type:ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter #type:ignore
from langchain_community.vectorstores import FAISS #type:ignore
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utlis.model_loader import ModelLoader



class DocumentIngestor:
    """_summary_

    Raises:
        DocumentPortalException: _description_
        DocumentPortalException: _description_
        DocumentPortalException: _description_
        DocumentPortalException: _description_

    Returns:
        _type_: _description_
    """
    SUPPORTED_FILE_TYPES = {'.pdf', '.txt', '.docx', '.md'}
    
    def __init__(self, data_dir = "data/multi_doc_chat", faiss_dir = "faiss_index", session_id=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.file_path = Path(data_dir)
            self.file_path.mkdir(parents=True, exist_ok=True)

            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            # sessionized paths
            self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_file_path = self.file_path / self.session_id
            self.session_faiss_path = self.faiss_dir / self.session_id
            self.session_file_path.mkdir(parents=True, exist_ok=True)
            self.session_faiss_path.mkdir(parents=True, exist_ok=True)

            self.model_loader = ModelLoader()
            self.log.info("DocumentIngestor initialized successfully", 
                        file_path=str(self.file_path),
                        faiss_path=str(self.faiss_dir),
                        session_file_path=str(self.session_file_path),
                        session_faiss_path=str(self.session_faiss_path),
                        model_loader=str(self.model_loader),
                        supported_file_types=self.SUPPORTED_FILE_TYPES,
                        session_id=self.session_id)
        except Exception as e:
            self.log.error(f"Error in initiating DocumentIngestor", error=str(e))
            raise DocumentPortalException("Error in initiating DocumentIngestor", sys)
    
    def ingest_files(self, uploaded_files):
        try:
            # Implement logic to ingest files here
            documents = []
            for uploaded_file in uploaded_files:
                ext=Path(uploaded_file.name).suffix.lower()

                if ext not in self.SUPPORTED_FILE_TYPES:
                    self.log.warning(f"File type {ext} not supported, hence skipping", filename = uploaded_file.name)
                    continue
                
                unique_filename = f"{uuid.uuid4().hex[:8]}{ext}"
                temp_path = self.session_file_path / unique_filename

                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                
                self.log.info(f"File saved successfully",
                            filename = uploaded_file.name,
                            temp_path = str(temp_path),
                            session_id = self.session_id)
        
                if ext == ".pdf":
                    loader = PyPDFLoader(str(temp_path))
                elif ext == ".txt":
                    loader = TextLoader(str(temp_path), encoding = "utf-8")
                elif ext == ".docx":
                    loader = Docx2txtLoader(str(temp_path))
                else:
                    self.log.warning(f"File type {ext} not supported", filename = uploaded_file.name)
                    continue
                docs = loader.load()
                documents.extend(docs)

            if not documents:
                self.log.warning("No documents found to ingest")
                raise DocumentPortalException("No documents found to ingest", sys)
            
            self.log.info("Documents loaded successfully", count = len(documents), session_id = self.session_id)
            return self._create_retriever(documents)

        except Exception as e:
            self.log.error(f"Error in ingesting files", error=str(e))
            raise DocumentPortalException("Error in ingesting files", sys)
        
    def _create_retriever(self, documents):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            self.log.info("Creating retriever", session_id = self.session_id, splitter_type = type(text_splitter))

            chunks = text_splitter.split_documents(documents)
            self.log.info("Split the documents successfully", count = len(chunks), session_id = self.session_id)

            vectorstore = FAISS.from_documents(documents = chunks, 
                                            embedding = self.model_loader.load_embeddings())
            self.log.info("Created the vector store successfully", session_id = self.session_id)

            vectorstore.save_local(str(self.session_faiss_path))
            self.log.info("Saved the vector store successfully",
                        session_id = self.session_id,
                        faiss_path = str(self.session_faiss_path))

            retriever = vectorstore.as_retriever(search_type = "similarity",search_kwargs={"k": 5})
            self.log.info("Created the retriever successfully",
                        session_id = self.session_id,
                        retriever_type = type(retriever))

            return retriever
        
        except Exception as e:
            self.log.error(f"Error in creating retriever", error=str(e))
            raise DocumentPortalException("Error in creating retriever", sys)



