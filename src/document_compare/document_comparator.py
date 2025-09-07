import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utlis.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentComparatorLLM:
    """
    A class to compare two documents using a language model and extract structured metadata & summary.
    """
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.prompt = PROMPT_REGISTRY['document_comparison']
        self.llm = ModelLoader().load_llm()
        self.parser = JsonOutputParser(pydantic_object=Metadata)
        self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
        self.chain = self.prompt | self.llm | self.fixing_parser
        self.log.info("DocumentComparatorLLM initialized successfully with Model and Parser")

    def compare_documents(self, document1: str, document2: str) -> dict:
        """
        Compare two documents and extract structured metadata & summary.
        """
        try:
            # Load the model
            loader = ModelLoader()
            llm = loader.load_llm()

            # Prepare parsers
            parser = JsonOutputParser(pydantic_object=Metadata)
            fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

            # Load the prompt
            prompt = PROMPT_REGISTRY['document_comparison']

            # Initialize the chain
            chain = prompt | llm | fixing_parser

            # Invoke the chain
            response = chain.invoke({
                "format_instructions": parser.get_format_instructions(),
                "document1": document1,
                "document2": document2
            })

            # Log the success
            CustomLogger().get_logger(__name__).info("Document comparison successful", keys=list(response.keys()))

            return response

        except Exception as e:
            # Log the error
            self.log.error("Document comparison failed", error=str(e))
            raise DocumentPortalException("Document comparison failed", sys)

    def _format_response(self, response: dict) -> dict:
        """
        Format the response to a dictionary.
        """
        try:
            # Convert the response to a dictionary
            response_dict = response.dict()

            # Log the success
            CustomLogger().get_logger(__name__).info("Response formatting successful", keys=list(response_dict.keys()))

            return response_dict

        except Exception as e:
            # Log the error
            self.log.error("Response formatting failed", error=str(e))
            raise DocumentPortalException("Response formatting failed", sys))