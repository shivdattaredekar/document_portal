import os
import sys
from utlis.model_loader import ModelLoader
from model.models import * 
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_library import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentAnalyzer:
    """
    Analyzes documents using a pretrained model
    Automatically logs all actions and supports session-based organizations
    """
    def __init__(self):
        """
        Raises:
            DocumentPortalException: _description_
        """
        
        self.log = CustomLogger.get_logger(__name__)
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()
            
            # Prepare parsers
            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm = self.llm)
            self.prompt = prompt
            
            self.log.info(f"Document analyzer initilized successfully")   

        except Exception as e:
            self.log.error(f"Error cased while initilizing the Document analyzer:{e}")
            raise DocumentPortalException(f"Failed to load the DocumentAnalyzer", e) from e
        
        
    def analyze_document(self, document_text:str)->dict:
        """
        Analyze document text and extract structured metadata & summary.
        Args:
            document_text (str): text extracted from the document

        Returns:
            dict: _description_
        """
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("MetaData analysis chain initilized")
            
            response = chain.invoke(
                {
                    'format_instructions': self.parser.get_format_instructions(),
                    'document_text': document_text
                }
            )
            
            self.log.info(f"Metadata extraction is successful", keys=list(response.keys()))
            return response
        
        except Exception as e:
            self.log.error("Error caused while analyzing the Document", error=str(e))
            raise DocumentPortalException(f'failed to analyze the document', e) from e 
        