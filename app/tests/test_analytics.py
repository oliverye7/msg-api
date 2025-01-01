import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.schemas.analytics import MessageStats, WordFrequency, WordFrequencyList
from app.tests.utils import mock_auth_dependencies

client = TestClient(app)

@pytest.fixture
def mock_imessage_db():
    """Mock the IMessageDB class."""
    with patch('app.api.v1.endpoints.analytics.IMessageDB') as mock:
        # Configure the mock
        instance = mock.return_value.__enter__.return_value
        
        # Mock message count method
        instance.get_message_count_by_contact.return_value = {
            "sent": 42,
            "received": 24
        }
        
        # Mock word frequency method
        instance.get_word_frequency.return_value = [
            ("hello", 10),
            ("world", 8),
            ("test", 5)
        ]
        
        yield mock



def test_get_contact_stats(mock_imessage_db, mock_auth_dependencies):
    """Test getting message statistics for a contact."""
    response = client.get("/api/v1/analytics/contacts/+1234567890/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert data == {"sent": 42, "received": 24}

def test_get_word_frequency(mock_imessage_db, mock_auth_dependencies):
    """Test getting word frequency for a contact."""
    response = client.get("/api/v1/analytics/contacts/+1234567890/word-frequency")
    assert response.status_code == 200
    
    data = response.json()
    assert "frequencies" in data
    frequencies = data["frequencies"]
    assert len(frequencies) == 3
    assert frequencies[0] == {"word": "hello", "count": 10}
    assert frequencies[1] == {"word": "world", "count": 8}
    assert frequencies[2] == {"word": "test", "count": 5}

def test_get_word_frequency_with_limit(mock_imessage_db, mock_auth_dependencies):
    """Test getting word frequency with custom limit."""
    # Configure mock to return only 2 items
    mock_instance = mock_imessage_db.return_value.__enter__.return_value
    mock_instance.get_word_frequency.return_value = [
        ("hello", 10),
        ("world", 8)
    ]
    
    response = client.get("/api/v1/analytics/contacts/+1234567890/word-frequency?limit=2")
    assert response.status_code == 200
    
    data = response.json()
    assert "frequencies" in data
    frequencies = data["frequencies"]
    assert len(frequencies) == 2
    assert frequencies[0] == {"word": "hello", "count": 10}
    assert frequencies[1] == {"word": "world", "count": 8}

def test_contact_not_found(mock_imessage_db, mock_auth_dependencies):
    """Test behavior when contact is not found."""
    mock_db_instance = mock_imessage_db.return_value.__enter__.return_value
    mock_db_instance.get_message_count_by_contact.return_value = {"sent": 0, "received": 0}
    mock_db_instance.get_word_frequency.return_value = []
    
    response = client.get("/api/v1/analytics/contacts/nonexistent/stats")
    assert response.status_code == 200
    assert response.json() == {"sent": 0, "received": 0}
    
    response = client.get("/api/v1/analytics/contacts/nonexistent/word-frequency")
    assert response.status_code == 200
    assert response.json() == {"frequencies": []}

def test_database_error(mock_imessage_db, mock_auth_dependencies):
    """Test handling of database errors."""
    mock_db_instance = mock_imessage_db.return_value.__enter__.return_value
    mock_db_instance.get_message_count_by_contact.side_effect = FileNotFoundError("DB not found")
    
    response = client.get("/api/v1/analytics/contacts/+1234567890/stats")
    assert response.status_code == 503
    assert "iMessage database not accessible" in response.json()["detail"]

def test_unauthorized_access(mock_imessage_db):
    """Test that endpoints require authentication."""
    # Test without auth dependencies mocked
    response = client.get("/api/v1/analytics/contacts/+1234567890/stats")
    assert response.status_code == 401
    
    response = client.get("/api/v1/analytics/contacts/+1234567890/word-frequency")
    assert response.status_code == 401