from pydantic import BaseModel, Field

class SearchParams(BaseModel):
    query: str =  Field(..., min=1, max=20)
    k: int = Field(5, gt=1, le=100)