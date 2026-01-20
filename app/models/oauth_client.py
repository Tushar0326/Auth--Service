import uuid
from sqlalchemy import Column, String, Boolean
from app.db.base import Base


class OAuthClient(Base):
    __tablename__ = "oauth_clients"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, unique=True, index=True)
    client_secret = Column(String)
    redirect_uri = Column(String)
    is_confidential = Column(Boolean, default=True)
