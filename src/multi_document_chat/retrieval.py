import os
import sys
from dotenv import load_dotenv #type:ignore
from langchain_core.chat_history import BaseChatMessageHistory #type:ignore
from langchain_community.chat_message_histories import ChatMessageHistory #type:ignore
from langchain_core.runnables.history import RunnableWithMessageHistory #type:ignore
from langchain_community.vectorstores import FAISS #type:ignore
from langchain.chains import create_history_aware_retriever, create_retrieval_chain #type:ignore
from langchain.chains.combine_documents import create_stuff_documents_chain #type:ignore
from langchain_core.output_parsers import StrOutputParser #type:ignore
from langchain_core.messages import BaseMessage #type:ignore
from utlis.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from model.models import PromptType
from prompt.prompt_library import PROMPT_REGISTRY
from operator import itemgetter
from typing import List, Optional



class ConversationalRAG:
    def __init__(self, session_id:str, retriever=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.llm = self._load_llm()
            self.contextualize_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            
            if retriever is None:
                self._load_retriever_from_from_faiss()
                self.log.info("Created retriever from local vectorstore")
    
            self.retriever = retriever        
            self._build_lecl_chain()
            self.log.info("ConversationalRAG initialized successfully", session_id=self.session_id)

            
        except Exception as e:
            self.log.error(f"Error in initiating ConversaionalRAG", error=str(e))
            raise DocumentPortalException("Error in initiating ConversaionalRAG", sys)
    
    def load_retriever_from_from_faiss(self, index_path):
        """_summary_

        Args:
            file_path (_type_): _description_

        Raises:
            DocumentPortalException: _description_
        """
        try:
            # Implement logic to load retriever from FAISS here
            embedding_model = ModelLoader().load_embedding_model()

            if os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory does not exist{index_path}")
            
            vectorstore = FAISS.load_local(
                            index_path,
                            embedding_model,
                            allow_dangerous_deserialization=True
                            )
            
            self.retriever = vectorstore.as_retriever(
                search_type = 'similarity',
                search_kwargs = {'k': 5}
            )
            self.log.info(
                        "Loaded retriever from FAISS index",
                        index_path = index_path,
                        session_id=self.session_id
                        )
            self._build_lecl_chain()
            return self.retriever
            
        except Exception as e:
            self.log.error(f"Error in loading retriever from FAISS", error=str(e))
            raise DocumentPortalException("Error in loading retriever from FAISS", sys)
    
    def invoke(self,
            user_input:str,
            chat_history:Optional[List[BaseMessage]]=None
            )->str:
        """

        Args:
            user_input (str): _description_
            chat_history (_type_, optional): _description_. Defaults to Optional[List[BaseMessage]]=None.

        Raises:
            DocumentPortalException: _description_

        Returns:
            str: _description_
        """
        try:
            answer = self.chain.invoke(
                {
                    "input": user_input,
                    "chat_history":chat_history if chat_history else []
                },
                config={"configurable": {"session_id": self.session_id}}
            )

            if not answer:
                self.log.warning("No answer found from the RAG chain", session_id=self.session_id)

            self.log.info("Invoked the ConversationalRAG",
                        session_id=self.session_id,
                        user_input=user_input,
                        preview_answer=answer[:100]
                        )
            return answer

        except Exception as e:
            self.log.error(f"Error in invoking Conversational RAG", error=str(e))
            raise DocumentPortalException("Error in invoking Conversational RAG", sys)
        
    def _load_llm(self):
        try:
            # Implement logic to load LLM here
            model = ModelLoader().load_llm()
            self.log.info("Loaded LLM",
                        session_id=self.session_id,
                        model_name=model.__class__.__name__)
            return model
        except Exception as e:
            self.log.error(f"Error in loading LLM", error=str(e))
            raise DocumentPortalException("Error in loading LLM", sys)
        
    def _format_docs(self, docs):
        try:
            "\n\n".join(doc.page_content for doc in docs)
        except Exception as e:
            self.log.error(f"Error in formatting documents", error=str(e))
            raise DocumentPortalException("Error in formatting documents", sys)
        
    def _build_lecl_chain(self):
        try:
            # Implement logic to build LCEL chain here
            
            question_rewriter = (
                {
                    "input":itemgetter("input"),
                    "chat_history": itemgetter("chat_history")
                }    
                | self.contextualize_prompt
                | self.llm
                | StrOutputParser()
            )

            retrieve_docs = question_rewriter | self.retriever | self._format_docs 

            self.chain = ({
                "context": retrieve_docs,
                "input": itemgetter("input"),
                "chat_history": itemgetter("chat_history")
            }
            | self.qa_prompt
            | self.llm
            | StrOutputParser()
            )
            self.log.info("Built LCEL chain", session_id=self.session_id)

        except Exception as e:
            self.log.error(f"Error in building LCEL chain", error=str(e))
            raise DocumentPortalException("Error in building LCEL chain", sys)