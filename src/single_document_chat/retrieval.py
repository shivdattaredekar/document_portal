import os
import sys
from dotenv import load_dotenv #type:ignore
from langchain_core.chat_history import BaseChatMessageHistory #type:ignore
from langchain_community.chat_message_histories import ChatMessageHistory #type:ignore
from langchain_core.runnables.history import RunnableWithMessageHistory #type:ignore
from langchain_community.vectorstores import FAISS #type:ignore
from langchain.chains import create_history_aware_retriever, create_retrieval_chain #type:ignore
from langchain.chains.combine_documents import create_stuff_documents_chain #type:ignore
from utlis.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from model.models import PromptType
from prompt.prompt_library import PROMPT_REGISTRY

class ConversationalRAG:
    def __init__(self, session_id:str, retriever):
            try:
                self.log = CustomLogger().get_logger(__name__)
                self.session_id = session_id
                self.retriever = retriever
                self.llm = self._load_llm()
                self.contextualize_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
                self.qa_prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
                self.history_aware_retriever = create_history_aware_retriever(
                    llm=self.llm, 
                    retriever=self.retriever, 
                    prompt=self.contextualize_prompt
                )
                self.log.info("Created the history aware retriever successfully", retriever_type=str(type(self.history_aware_retriever)))
                self.qa_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
                self.rag_chain = create_retrieval_chain(self.history_aware_retriever, self.qa_chain)
                self.log.info("Created the RAG chain successfully", chain_type=str(type(self.rag_chain)))

                self.chain = RunnableWithMessageHistory(
                    self.rag_chain,
                    self._get_session_history,
                    input_messages_key="input",
                    history_messages_key="chat_history",
                    output_messages_key="answer"
                )
                self.log.info("Created the RunnableWithMessageHistory", chain_type=str(type(self.chain)))

            except Exception as e:
                self.log.error("Failed to initialize the ConversationalRAG",error=str(e))
                raise DocumentPortalException("Failed to initialize the ConversationalRAG",sys)
        
    def _load_llm(self):
        try:
            llm = ModelLoader().load_llm()
            self.log.info("Loaded the LLM successfully", llm_type=str(type(llm)), Model_name = llm.__class__.__name__)
            return llm
        except Exception as e:
            self.log.error("Failed to load the LLM", error=str(e))
            raise DocumentPortalException("Failed to load the LLM", sys)
        
    def _get_session_history(self, session_id: str):
        try:
            return ChatMessageHistory()

        except Exception as e:
            self.log.error("Failed to get the session history", session_id=session_id ,error=str(e))
            raise DocumentPortalException("Failed to get the session history", sys)
    
    def load_retriever_from_faiss(self, index_path:str):
        try:
            embeddings = ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory does not exist{index_path}")

            vectorstore = FAISS.load_local(index_path, embeddings)
            self.log.info("Loaded retriever from FAISS index", index_path = index_path)
            return vectorstore.as_retriever(search_type = "similarity",search_kwargs={"k": 5})

        except Exception as e:
            self.log.error("Failed to load the retriever from FAISS", error=str(e))
            raise DocumentPortalException("Failed to load the retriever from FAISS", sys)
    
    def invoke(self, user_input:str)->str:
        try:    
            response = self.chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": self.session_id}}
            )
            answer = response.get("answer", "No answer.")
            
            if not answer:
                self.log.warning("No answer found from the RAG chain", session_id=self.session_id)
            
            self.log.info("Invoked the ConversationalRAG", session_id=self.session_id, 
                        user_input=user_input, preview_answer=answer[:100])
            return answer 
        
        except Exception as e:
            self.log.error("Failed to invoke the ConversationalRAG", error=str(e), session_id=self.session_id)
            raise DocumentPortalException("Failed to invoke the ConversationalRAG", sys)