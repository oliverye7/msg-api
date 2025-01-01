import os
import pytest
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.imessage import Base, Message, Handle, Chat
from app.db.imessage import IMessageDB

@pytest.fixture
def test_db():
    """Create a temporary test database."""
    # Create a temporary file
    db_fd, db_path = tempfile.mkstemp()
    
    # Create the database and tables
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    
    # Create a session factory
    SessionLocal = sessionmaker(bind=engine)
    
    # Add test data
    with SessionLocal() as session:
        # Create test handles (contacts)
        handle1 = Handle(
            contact_id="+1234567890",
            service="iMessage",
            country="US"
        )
        handle2 = Handle(
            contact_id="test@example.com",
            service="iMessage",
            country="US"
        )
        session.add_all([handle1, handle2])
        session.flush()
        
        # Create test messages
        messages = [
            Message(
                guid="msg1",
                text="Hello world",
                handle_id=handle1.id,
                is_from_me=1,
                date=1000
            ),
            Message(
                guid="msg2",
                text="How are you?",
                handle_id=handle1.id,
                is_from_me=0,
                date=2000
            ),
            Message(
                guid="msg3",
                text="Hello world again",
                handle_id=handle1.id,
                is_from_me=1,
                date=3000
            ),
            # Messages for second handle
            Message(
                guid="msg4",
                text="Different contact",
                handle_id=handle2.id,
                is_from_me=0,
                date=4000
            )
        ]
        session.add_all(messages)
        session.commit()
    
    yield db_path
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

def test_message_count(test_db):
    """Test getting message counts for a contact."""
    with IMessageDB(test_db) as db:
        # Test first contact
        counts = db.get_message_count_by_contact("+1234567890")
        assert counts["sent"] == 2  # Messages from me
        assert counts["received"] == 1  # Messages to me
        
        # Test second contact
        counts = db.get_message_count_by_contact("test@example.com")
        assert counts["sent"] == 0
        assert counts["received"] == 1
        
        # Test non-existent contact
        counts = db.get_message_count_by_contact("nonexistent")
        assert counts["sent"] == 0
        assert counts["received"] == 0

def test_word_frequency(test_db):
    """Test getting word frequency for a contact."""
    with IMessageDB(test_db) as db:
        # Test first contact
        frequencies = db.get_word_frequency("+1234567890")
        # Convert to dict for easier testing
        freq_dict = dict(frequencies)
        assert freq_dict["hello"] == 2
        assert freq_dict["world"] == 2
        assert freq_dict["how"] == 1
        assert freq_dict["are"] == 1
        assert freq_dict["you"] == 1
        
        # Test non-existent contact
        frequencies = db.get_word_frequency("nonexistent")
        assert len(frequencies) == 0

def test_database_context_manager(test_db):
    """Test that the database context manager works correctly."""
    with IMessageDB(test_db) as db:
        assert db.engine is not None
        assert db.SessionLocal is not None
        
    # After context manager exits
    assert not os.path.exists(db.temp_db_path)