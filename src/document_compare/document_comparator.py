import sys
from dotenv import load_dotenv # type:ignore
import pandas as pd # type:ignore
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utlis.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser # type:ignore
from langchain.output_parsers import OutputFixingParser # type:ignore
from model.models import Metadata

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
        self.chain = self.prompt | self.llm
        self.log.info("DocumentComparatorLLM initialized successfully with Model and Parser")

    def compare_documents(self, combined_docs:str) -> pd.DataFrame:
        """
        Compare two documents and extract structured metadata & summary.
        """
        try:
            inputs={
                "combined_docs":combined_docs,
                "format_instruction":self.parser.get_format_instructions()
            }
            self.log.info("Document comparison started", inputs=inputs)
            response = self.chain.invoke(inputs)
            self.log.info("Document comparison successful", response=response)
            return self._format_response(response)
            

        except Exception as e:
            # Log the error
            self.log.error("Document comparison failed", error=str(e))
            raise DocumentPortalException("Document comparison failed", sys)

    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame:
        """
        Format the response to a dictionary.
        """
        try:
            df = pd.DataFrame(response_parsed)
            self.log.info("Response formatting started", dataframe=df)
            return df

        except Exception as e:
            # Log the error
            self.log.error("Response formatting failed", error=str(e))
            raise DocumentPortalException("Response formatting failed", sys)