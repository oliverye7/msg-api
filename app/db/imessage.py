import os
import shutil
import sqlite3
import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import text
from pathlib import Path

from app.models.imessage import Base, Message, Handle, Chat

class IMessageDB:
    def __init__(self, db_path: Optional[str] = None):
        """Initialize iMessage database connection.
        
        Args:
            db_path: Path to iMessage database. If None, uses default location.
        """
        self.original_db_path = db_path or os.path.expanduser("~/Library/Messages/chat.db")
        self.temp_db_path = "/tmp/chat_temp.db"
        self.engine = None
        self.SessionLocal = None

    def connect(self) -> None:
        """Create a safe copy of the database and establish connection."""
        if not os.path.exists(self.original_db_path):
            raise FileNotFoundError(f"iMessage database not found at {self.original_db_path}")
        
        # Create a copy of the database to avoid locking the original
        shutil.copy2(self.original_db_path, self.temp_db_path)
        
        # Create SQLAlchemy engine and session
        self.engine = create_engine(f"sqlite:///{self.temp_db_path}")
        self.SessionLocal = sessionmaker(bind=self.engine)

    def close(self) -> None:
        """Close connection and clean up temporary database."""
        if self.engine:
            self.engine.dispose()
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def get_message_count_by_contact(self, contact_id: str) -> Dict[str, int]:
        """Get total messages sent and received for a specific contact.
        
        Args:
            contact_id: Phone number or email of the contact
            
        Returns:
            Dict containing sent and received message counts
        """
        with self.SessionLocal() as session:
            handle = session.query(Handle).filter(Handle.contact_id == contact_id).first()
            if not handle:
                return {"sent": 0, "received": 0}
            
            sent = session.query(Message).filter(
                Message.handle_id == handle.id,
                Message.is_from_me == 1
            ).count()
            
            received = session.query(Message).filter(
                Message.handle_id == handle.id,
                Message.is_from_me == 0
            ).count()
            
            return {"sent": sent, "received": received}

    def _tokenize_text(self, text: str) -> List[str]:
        """Convert text into a list of cleaned words.
        
        Args:
            text: Input text string
            
        Returns:
            List of cleaned words
        """
        # Convert to lowercase and split on whitespace
        text = text.lower()
        
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text)
        
        return words

    def get_word_frequency(self, contact_id: str, limit: int = 10) -> List[Tuple[str, int]]:
        """Get most common words used in conversations with a contact.
        
        Args:
            contact_id: Phone number or email of the contact
            limit: Number of top words to return
            
        Returns:
            List of (word, frequency) tuples
        """
        with self.SessionLocal() as session:
            handle = session.query(Handle).filter(Handle.contact_id == contact_id).first()
            if not handle:
                return []
            
            # Get all messages for this contact
            messages = session.query(Message.text).filter(
                Message.handle_id == handle.id,
                Message.text.isnot(None)  # Exclude null messages
            ).all()
            
            # Combine all messages and count words
            words = []
            for msg in messages:
                if msg.text:  # Additional null check
                    words.extend(self._tokenize_text(msg.text))
            
            # Count frequencies and return top N
            word_counts = Counter(words)
            return word_counts.most_common(limit)

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()