from langchain_core.output_parsers import JsonOutputParser # type:ignore
from model.models import Metadata
from utlis.model_loader import ModelLoader
from prompt.prompt_library import PROMPT_REGISTRY

parser= JsonOutputParser(pydantic_object=Metadata)

inputs={
        
        "format_instructions":parser.get_format_instructions()
    }

print(inputs)