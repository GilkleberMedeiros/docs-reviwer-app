from pydantic import BaseModel, Field


class DocMetadata(BaseModel):
    origin: str
    available: bool = Field(default_factory=lambda : bool(True))
