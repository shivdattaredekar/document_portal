import os
import sys
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.vectorstores import FAISS
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from model.models import PromptType
from prompt.prompt_library import PROMPT_REGISTRY

class ConversationalRAG:
    def __init__(self):
            try:
                self.log = CustomLogger().get_logger(__name__)
            except Exception as e:
                self.log.error("Failed to initialize the ConversationalRAG",error=str(e))
                raise DocumentPortalException("Failed to initialize the ConversationalRAG",sys)
        
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to load the LLM", error=str(e))
            raise DocumentPortalException("Failed to load the LLM", sys)
        
    def _get_session_history(self, session_id: str):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to get the session history", session_id=session_id ,error=str(e))
            raise DocumentPortalException("Failed to get the session history", sys)
    
    def _load_retriever_from_faiss(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to load the retriever from FAISS", error=str(e))
            raise DocumentPortalException("Failed to load the retriever from FAISS", sys)
    
    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to invoke the ConversationalRAG", error=str(e), session_id=session_id)
            raise DocumentPortalException("Failed to invoke the ConversationalRAG", sys)