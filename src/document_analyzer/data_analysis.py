import os
from utlis.model_loader import ModelLoader
from model.models import * 
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser


class DocumentAnalyzer:
    """
    Analyzes documents using a pretrained model
    Automatically logs all actions and supports session-based organizations
    """
    def __init__(self):
        pass
    def analyze_metadata(self):
        pass