"""file containing document model."""

from pydantic import BaseModel


class Document(BaseModel):
    """Document model for representing insurance documents."""
    source: str
    content: str
    clean_content: str
    pages: int
    characters: int
    language: str | None = None
