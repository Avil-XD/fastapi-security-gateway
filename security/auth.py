from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import time
from typing import Optional, Dict

security = HTTPBearer()
rate_limits: Dict[str, Dict[str, float]] = {}

from fastapi import Request
from pydantic import BaseModel

class TokenData(BaseModel):
    sub: str
    exp: float
    is_admin: bool = False

class SecurityManager:
    def __init__(self, secret_key: str, rate_limit: int = 100, window: int = 60):
        self.secret_key = secret_key
        self.rate_limit = rate_limit
        self.window = window
        
    async def authenticate_request(self, 
                                credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
        """Authenticate and validate JWT token"""
        try:
            token = credentials.credentials
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            
            # Check if token is expired
            if payload.get('exp', 0) < time.time():
                raise HTTPException(
                    status_code=401,
                    detail="Token has expired"
                )
                
            # Rate limiting
            user_id = payload.get('sub')
            if not self._check_rate_limit(user_id):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded"
                )
                
            return payload
            
        except jwt.JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
            
    def _check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limit"""
        current_time = time.time()
        
        if user_id not in rate_limits:
            rate_limits[user_id] = {
                'count': 1,
                'window_start': current_time
            }
            return True
            
        user_limits = rate_limits[user_id]
        
        # Check if window has expired
        if current_time - user_limits['window_start'] > self.window:
            # Reset window
            user_limits.update({
                'count': 1,
                'window_start': current_time
            })
            return True
            
        # Check if user has exceeded rate limit
        if user_limits['count'] >= self.rate_limit:
            return False
            
        # Increment request count
        user_limits['count'] += 1
        return True
        
    def create_access_token(self, user_id: str, expires_delta: Optional[int] = None) -> str:
        """Create new JWT token"""
        payload = {
            'sub': user_id,
            'iat': time.time(),
            'exp': time.time() + (expires_delta or 3600)  # Default 1 hour
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
        
    def verify_admin(self, token_payload: dict) -> bool:
        """Verify if user has admin privileges"""
        return token_payload.get('is_admin', False)
        
# Dependency for protected routes
async def get_current_user(
    security_manager: SecurityManager,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """Validate user token and return user info"""
    return await security_manager.authenticate_request(credentials)

# Dependency for admin-only routes
async def get_admin_user(
    security_manager: SecurityManager,
    user: dict = Depends(get_current_user)
) -> dict:
    """Validate admin privileges"""
    if not security_manager.verify_admin(user):
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )
    return user