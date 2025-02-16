"""
Minimal example demonstrating core security gateway features.
Run this file directly to test basic functionality.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import jwt
import os
from datetime import datetime, timedelta

# Initialize FastAPI
app = FastAPI(title="Security Gateway Demo")
security = HTTPBearer()

# Simple in-memory rate limiting
request_count = {}

def rate_limit(ip: str, limit: int = 100):
    """Basic rate limiting"""
    now = datetime.now()
    if ip in request_count:
        count, timestamp = request_count[ip]
        if (now - timestamp).seconds >= 60:  # Reset after 1 minute
            request_count[ip] = (1, now)
        elif count >= limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        else:
            request_count[ip] = (count + 1, timestamp)
    else:
        request_count[ip] = (1, now)

def create_jwt_token():
    """Create a sample JWT token"""
    secret = os.getenv("JWT_SECRET", "demo-secret-key")
    expiration = datetime.utcnow() + timedelta(minutes=15)
    token = jwt.encode(
        {"sub": "demo-user", "exp": expiration},
        secret,
        algorithm="HS256"
    )
    return token

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        secret = os.getenv("JWT_SECRET", "demo-secret-key")
        payload = jwt.decode(credentials.credentials, secret, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def root():
    """Public endpoint"""
    return {"message": "Welcome to Security Gateway Demo"}

@app.post("/token")
async def get_token(client_ip: str = "127.0.0.1"):
    """Get a sample JWT token"""
    rate_limit(client_ip)  # Apply rate limiting
    token = create_jwt_token()
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected")
async def protected_route(payload: dict = Depends(verify_jwt_token),
                        client_ip: str = "127.0.0.1"):
    """Protected endpoint requiring JWT authentication"""
    rate_limit(client_ip)  # Apply rate limiting
    return {
        "message": "Access granted to protected route",
        "user": payload["sub"]
    }

if __name__ == "__main__":
    print("\n🔒 Security Gateway Demo")
    print("------------------------")
    print("1. Visit http://localhost:8000/docs for interactive API documentation")
    print("2. Get a token from POST /token")
    print("3. Use the token to access GET /protected")
    print("------------------------\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)