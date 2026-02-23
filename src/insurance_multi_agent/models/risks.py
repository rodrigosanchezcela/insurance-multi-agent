from pydantic import BaseModel
from typing import List


class Risks(BaseModel):
    risks : List[str]