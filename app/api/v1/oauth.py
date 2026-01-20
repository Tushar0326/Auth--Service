from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import secrets
from datetime import datetime, timedelta

from app.core.jwt import create_access_token
from app.db.deps import get_db
from app.models.auth_code import AuthorizationCode
from app.models.oauth_client import OAuthClient
from app.core.auth import get_current_user

router = APIRouter(prefix="/oauth", tags=["OAuth2"])


@router.get("/authorize")
def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if response_type != "code":
        raise HTTPException(400, "Invalid response type")

    client = db.query(OAuthClient).filter_by(client_id=client_id).first()
    if not client or client.redirect_uri != redirect_uri:
        raise HTTPException(400, "Invalid client")

    code_value = secrets.token_urlsafe(32)

    code = AuthorizationCode(
        code=code_value,
        user_id=user.id,
        client_id=client_id,
        redirect_uri=redirect_uri,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )

    db.add(code)
    db.commit()

    redirect_url = f"{redirect_uri}?code={code_value}"
    if state:
        redirect_url += f"&state={state}"

    return RedirectResponse(redirect_url)

@router.post("/token")
def token(
    grant_type: str,
    code: str,
    redirect_uri: str,
    client_id: str,
    client_secret: str,
    db: Session = Depends(get_db),
):
    if grant_type != "authorization_code":
        raise HTTPException(400, "Invalid grant type")

    client = db.query(OAuthClient).filter_by(client_id=client_id).first()
    if not client or client.client_secret != client_secret:
        raise HTTPException(401, "Invalid client credentials")

    auth_code = db.query(AuthorizationCode).filter_by(code=code).first()

    if not auth_code or auth_code.expires_at < datetime.utcnow():
        raise HTTPException(400, "Invalid or expired code")

    access_token = create_access_token(
        data={"sub": auth_code.user_id}
    )

    db.delete(auth_code)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/userinfo")
def userinfo(user=Depends(get_current_user)):
    return {
        "sub": user.id,
        "email": user.email,
    }