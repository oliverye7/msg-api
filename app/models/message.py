from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, BigInteger, Index
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class Contact(Base, TimestampMixin):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    handle_id = Column(String, unique=True, nullable=False)  # Original handle_id from iMessage
    
    # Metadata
    total_messages = Column(Integer, default=0)
    last_message_date = Column(DateTime, nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="contact")

class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    imessage_id = Column(BigInteger, unique=True, nullable=False)  # Original ROWID from iMessage
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    text = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    is_from_me = Column(Integer, nullable=False)  # 0 or 1
    
    # Relationships
    contact = relationship("Contact", back_populates="messages")

class MessageAnalytics(Base, TimestampMixin):
    __tablename__ = "message_analytics"

    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    word = Column(String, nullable=False)
    frequency = Column(Integer, default=0)
    
    __table_args__ = (
        Index('idx_contact_word', contact_id, word),
    )
