from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.core.settings import settings
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session
import secrets

# OAuth setup
config = Config(environ={
    'GITHUB_CLIENT_ID': settings.GITHUB_CLIENT_ID,
    'GITHUB_CLIENT_SECRET': settings.GITHUB_CLIENT_SECRET,
})

oauth = OAuth(config)

# GitHub OAuth setup
oauth.register(
    name='github',
    api_base_url='https://api.github.com/',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    client_kwargs={'scope': 'user:email'}
)

# API key authentication


def generate_api_key():
    return secrets.token_urlsafe(32)


async def get_current_user(
    api_key: str = Depends(OAuth2AuthorizationCodeBearer(tokenUrl="token")),
    db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.api_key == api_key,
                                 User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key or inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
