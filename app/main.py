from fastapi import FastAPI
from app.config import settings
from app.db.session import engine
from app.db.base import Base
from app.api.v1.auth import router as auth_router 

app = FastAPI(
    title="OIDC Authentication Service",
    version="1.0.0",
    description="Authentication & Identity Provider"
)


@app.get("/")
def health_check():
    return {
         "app": settings.app_name,
        "env": settings.env
    }

print(settings.secret_key)

app = FastAPI(title=settings.app_name)


@app.get("/")
def health_check():
    return {
        "database": "connected",
        "db_url": settings.database_url
    }

app = FastAPI(title=settings.app_name)

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"status": "users table ready"}

app = FastAPI(title=settings.app_name)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)