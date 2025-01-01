from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ContactBase(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None
    handle_id: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    total_messages: int
    last_message_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    text: Optional[str]
    date: datetime
    is_from_me: int

class MessageCreate(MessageBase):
    imessage_id: int
    contact_id: int

class Message(MessageBase):
    id: int
    contact_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WordFrequency(BaseModel):
    word: str
    frequency: int

class MessageStats(BaseModel):
    total_messages: int
    messages_sent: int
    messages_received: int
    most_common_words: List[WordFrequency]
    first_message_date: Optional[datetime]
    last_message_date: Optional[datetime]