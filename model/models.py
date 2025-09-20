from pydantic import BaseModel, Field, RootModel #type:ignore
from typing import Annotated, List, Optional, Dict, Any, Union

class Metadata(BaseModel):
    Summary: List[str]
    Title: str
    Author: List[str]
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]  # Can be "Not Available"
    SentimentTone: str

class ChangeFormat(BaseModel):
    Page: str
    change: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass
    