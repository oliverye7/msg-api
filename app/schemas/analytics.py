from pydantic import BaseModel
from typing import List

class MessageStats(BaseModel):
    sent: int
    received: int

class WordFrequency(BaseModel):
    word: str
    count: int

class WordFrequencyList(BaseModel):
    frequencies: List[WordFrequency]