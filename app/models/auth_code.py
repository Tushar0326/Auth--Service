import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.base import Base


class AuthorizationCode(Base):
    __tablename__ = "authorization_codes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, unique=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    client_id = Column(String)
    redirect_uri = Column(String)
    expires_at = Column(DateTime)
