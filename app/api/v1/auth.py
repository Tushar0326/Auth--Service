from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.auth import get_current_user
from app.models.refresh_token import RefreshToken
from app.core.refresh import generate_refresh_token, get_refresh_expiry
from app.core.oidc import create_id_token


router = APIRouter(prefix="/api/v1", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

from datetime import datetime
from app.models.refresh_token import RefreshToken


@router.post("/refresh")
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )

    if not token or token.is_revoked:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Refresh token expired"
        )

    access_token = create_access_token(
        data={"sub": token.user_id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
