# OIDC-Compatible Authentication Microservice

A production-ready authentication and identity provider built using FastAPI, implementing OAuth 2.0, OpenID Connect (OIDC), JWT (RS256), JWKS, refresh tokens, key rotation, Docker, and OpenTelemetry.

This service is designed to function similarly to Auth0 / Keycloak at a smaller scale.

## 🚀 Features

✅ User registration & login
✅ Secure password hashing (bcrypt)
✅ JWT access tokens (RS256)

✅ Refresh token mechanism
✅ OAuth 2.0 Authorization Code Flow
✅ PKCE-ready architecture

✅ OpenID Connect Discovery
✅ JWKS endpoint for token verification
✅ RSA key rotation with kid

✅ Environment-based configuration
✅ Dockerized deployment
✅ OpenTelemetry tracing (optional)
✅ Clean microservice architecture

## 🧱 Architecture Overview
Client
   │
   ▼
Auth Service (FastAPI)
   ├── OAuth 2.0 Endpoints
   ├── OIDC Discovery
   ├── JWT Issuer (RS256)
   ├── JWKS Publisher
   ├── Refresh Token Store
   ├── Key Rotation System
   └── OpenTelemetry Tracing
        │
        ▼
     PostgreSQL

## 🔐 Authentication Flow

### 1️⃣ User Registration
POST /api/v1/register

Email & password stored securely
Password hashed using bcrypt

### 2️⃣ Login
POST /api/v1/login

Returns:
POST /api/v1/refresh

Issues new access token
Old refresh tokens invalidated safely

### 5️⃣ OIDC Discovery
GET /.well-known/openid-configuration

Used by:
- frontend apps
- mobile apps
- third-party services

### 6️⃣ JWKS
GET /.well-known/jwks.json

Public RSA keys exposed for token verification.

## 🔑 Key Rotation Strategy

The service supports zero-downtime key rotation.
### 1️⃣ Create virtual environment
APP_NAME=OIDC Auth Service
ENV=development
SECRET_KEY=super-secret-change-this-later
ALGORITHM=RS256

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=sqlite:///./auth.db
ENABLE_TELEMETRY=false
### Build image

- Password hashing using bcrypt
- RSA asymmetric JWT signing
- No shared secrets between services
- Key rotation support
- Refresh token revocation
- Strict environment configuration
- Token expiration enforced

## 📌 Future Enhancements

- 🔄 PKCE enforcement
- 👥 Role-based access control (RBAC)
- 🧩 Multi-tenant support
- 🔐 MFA / OTP
- 🌐 SSO integrations
- 📈 Metrics dashboard