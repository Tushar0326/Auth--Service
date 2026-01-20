from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass

# import all models here 
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.oauth_client import OAuthClient
from app.models.auth_code import AuthorizationCode

