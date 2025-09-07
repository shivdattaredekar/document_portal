import os
import sys
from dotenv import load_dotenv
from utlis.config_loader import load_config

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_groq.chat_models import ChatGroq
from langchain_openai.chat_models import ChatOpenAI

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    """
    A class to load and manage LLM and embeddings based on configuration settings.
    """
    
    def __init__(self):
        # Load the environment variables from .env file
        load_dotenv()
        self._validate_env()
        self.config = load_config('config/config.yaml')
        log.info("Configuration loaded successfully.", config_keys=list(self.config.keys()))

    def _validate_env(self):
        """
        Validate necessary environment variables are set.
        """
        required_vars = ['OPENAI_KEY', 'PINECONE_TOKEN', 'GROQ_API_KEY', 'SERPER_KEY', 'HF_TOKEN', 'LANGSMITH_KEY', 'GOOGLE_API_KEY']
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing_keys = [key for key, value in self.api_keys.items() if not value]
        if missing_keys:
            log.error(f"Missing required environment variables: {', '.join(missing_keys)}")
            raise DocumentPortalException(f"Missing required environment variables", sys)
        log.info("All required environment variables are set", available_keys=list(self.api_keys.keys()))
        
    def load_embeddings(self):
        """
        Load embeddings based on configuration.
        """
        try:
            log.info("Loading embeddings...")
            # google embedding
            model_name=self.config['embedding_model']['google']['model_name']
            return GoogleGenerativeAIEmbeddings(model=model_name)
            
        except Exception as e:
            log.error(f"Embedding model could be loaded due the : {str(e)}")
            raise DocumentPortalException(f'Failed to load the embedding model', sys)
        
    def load_llm(self):
        """
        Load model based on configuration
        """
        
        llm_block = self.config['llm']
        log.info('Loading LLM......')
        
        provider_key = os.getenv('LLM_PROVIDER', "groq")
        
        if provider_key not in llm_block:
            log.error("LLM provider not available in config", provider_key= provider_key)
            raise ValueError(f"Provider {provider_key} not in the config")
        
        llm_config = llm_block[provider_key]
        provider= llm_config.get('provider')
        model_name= llm_config.get('model_name')
        temperature= llm_config.get('temperature', 0.2)  
        max_tokens= llm_config.get('max_tokens', 2048)
        
        if provider == 'groq':
            llm = ChatGroq(
                api_key=os.getenv('GROQ_API_KEY'), 
                model=model_name, 
                temperature=temperature, 
                max_tokens=max_tokens
                        )
        elif provider == 'google':
            llm = ChatGoogleGenerativeAI(
                api_key=os.getenv('GOOGLE_API_KEY'), 
                model=model_name, 
                temperature=temperature, 
                max_tokens=max_tokens
            )
        else:
            llm = ChatOpenAI(
                api_key=os.getenv('OPENAI_KEY'), 
                model=model_name, 
                temperature=temperature, 
                max_tokens=max_tokens
            )
            
        return llm
    

if __name__ == '__main__':
    loader = ModelLoader()

    # Test Embedding
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result: {result}")