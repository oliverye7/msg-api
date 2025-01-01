from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuthError
from datetime import timedelta
from starlette.middleware.sessions import SessionMiddleware

from app.core.auth import oauth, create_access_token
from app.core.config import settings

router = APIRouter()


@router.get("/test")
async def test_route():
    return {"status": "ok"}


@router.get("/test2")
def test_route_sync():
    return {"status": "ok"}


@router.get("/login/github")
async def github_login(request: Request):
    try:
        # First return a simple response to test if the route works
        if request.headers.get("test-mode") == "true":
            return {"status": "route works"}
            
        # Use absolute URL since we know the structure
        redirect_uri = str(request.base_url)[:-1] + "/api/v1/auth/github/callback"
        print(f"Debug - Base URL: {request.base_url}")
        print(f"Debug - Redirect URI: {redirect_uri}")
        return await oauth.github.authorize_redirect(request, redirect_uri)
    except Exception as e:
        print(f"Debug - Error in github_login: {str(e)}")
        raise


@router.get("/github/callback")
async def github_auth(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request)
        resp = await oauth.github.get('user', token=token)
        user_info = resp.json()

        # Get user's email from GitHub
        emails_resp = await oauth.github.get('user/emails', token=token)
        emails = emails_resp.json()
        primary_email = next(email["email"]
                             for email in emails if email["primary"])

        # Create access token
        access_token = create_access_token(
            data={"sub": primary_email},
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except OAuthError as error:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth error: {error.error}"
        )
