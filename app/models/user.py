from sqlalchemy import Column, Integer, String, Enum, Boolean
from .base import Base, TimestampMixin
import enum

class AuthProvider(str, enum.Enum):
    GOOGLE = "google"
    GITHUB = "github"

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    auth_provider = Column(Enum(AuthProvider), nullable=False)
    provider_user_id = Column(String, nullable=False)  # ID from OAuth provider
    is_active = Column(Boolean, default=True)
    api_key = Column(String, unique=True, index=True)  # For API authentication