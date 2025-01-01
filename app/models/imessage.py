from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association tables
chat_message_assoc = Table(
    'chat_message_join', Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.ROWID')),
    Column('message_id', Integer, ForeignKey('message.ROWID')),
    Column('message_date', Integer)
)

chat_handle_assoc = Table(
    'chat_handle_join', Base.metadata,
    Column('chat_id', Integer, ForeignKey('chat.ROWID')),
    Column('handle_id', Integer, ForeignKey('handle.ROWID'))
)

class Handle(Base):
    """Model for contact/handle information."""
    __tablename__ = 'handle'

    id = Column('ROWID', Integer, primary_key=True)
    contact_id = Column('id', Text, nullable=False)  # Phone number or email
    country = Column(Text)
    service = Column(Text, nullable=False)  # iMessage, SMS, etc.
    
    # Relationships
    messages = relationship("Message", back_populates="handle")
    chats = relationship("Chat", secondary=chat_handle_assoc, back_populates="handles")

class Message(Base):
    """Model for messages."""
    __tablename__ = 'message'

    id = Column('ROWID', Integer, primary_key=True)
    guid = Column(Text, nullable=False)
    text = Column(Text)
    handle_id = Column(Integer, ForeignKey('handle.ROWID'))
    date = Column(Integer)  # Unix timestamp
    date_read = Column(Integer)
    date_delivered = Column(Integer)
    is_from_me = Column(Integer)
    is_read = Column(Integer)
    is_delivered = Column(Integer)
    
    # Relationships
    handle = relationship("Handle", back_populates="messages")
    chats = relationship("Chat", secondary=chat_message_assoc, back_populates="messages")

class Chat(Base):
    """Model for chat/conversation threads."""
    __tablename__ = 'chat'

    id = Column('ROWID', Integer, primary_key=True)
    guid = Column(Text, nullable=False)
    chat_identifier = Column(Text)  # Group chat name or contact identifier
    service_name = Column(Text)
    room_name = Column(Text)
    display_name = Column(Text)
    
    # Relationships
    messages = relationship("Message", secondary=chat_message_assoc, back_populates="chats")
    handles = relationship("Handle", secondary=chat_handle_assoc, back_populates="chats")