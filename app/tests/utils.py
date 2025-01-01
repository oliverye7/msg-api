import pytest
from typing import Dict, Any
from unittest.mock import AsyncMock
from fastapi import Depends
from app.core.auth import get_current_user

# Create a mock user for testing
TEST_USER = {"email": "test@example.com"}

async def mock_get_current_user():
    """Mock get_current_user dependency."""
    return TEST_USER

@pytest.fixture
def mock_auth_dependencies(monkeypatch):
    """Override auth dependencies for testing."""
    from app.api.v1.endpoints import analytics
    
    # Override the dependency in the analytics module
    analytics.get_current_user = mock_get_current_user
    
    # Override the dependency in FastAPI app
    from app.main import app
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    yield
    
    # Clean up after tests
    app.dependency_overrides = {}
