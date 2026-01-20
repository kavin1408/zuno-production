import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import json
import requests
import time

security = HTTPBearer()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")

# Cache keys to avoid fetching on every request
_jwks_cache = {}
_jwks_timestamp = 0

def get_jwks():
    global _jwks_cache, _jwks_timestamp
    
    # Refresh cache every hour
    if _jwks_cache and (time.time() - _jwks_timestamp < 3600):
        return _jwks_cache
        
    if not SUPABASE_URL:
        print("⚠️ SUPABASE_URL not set, cannot fetch JWKs")
        return None
        
    try:
        url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
        print(f"Fetching JWKs from {url}")
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            _jwks_cache = resp.json()
            _jwks_timestamp = time.time()
            return _jwks_cache
        else:
            print(f"Failed to fetch JWKs: {resp.status_code}")
    except Exception as e:
        print(f"Error fetching JWKs: {e}")
        
    return None

def get_current_user_claims(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verifies JWT and returns full payload claims"""
    token = credentials.credentials
    
    if not SUPABASE_JWT_SECRET:
        print("❌ CRITICAL: SUPABASE_JWT_SECRET is not set!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server authentication configuration error",
        )
    
    try:
        # 1. Peeking at the header to determine algorithm
        try:
            unverified_header = jwt.get_unverified_header(token)
            alg = unverified_header.get('alg')
        except:
             # If we can't even read the header, just let the standard decode fail
             alg = "HS256"

        key = str(SUPABASE_JWT_SECRET)
        algorithms = ["HS256"]
        
        # 2. If ES256 (new Supabase default), fetch JWKs
        if alg == 'ES256':
            jwks = get_jwks()
            if jwks:
                key = jwks
                algorithms = ["ES256"]
            else:
                 print("⚠️ Could not fetch JWKS for ES256 token, trying secret as fallback (will likely fail)")

        # 3. Decode
        if alg == 'ES256':
             # For ES256/JWK, we often pass the whole JWKS dict as 'key' in python-jose
             # It acts as a key set.
             payload = jwt.decode(
                token, 
                key, 
                algorithms=["ES256"], 
                options={
                    "verify_aud": False,
                    "verify_iss": False,
                    "verify_sub": True,
                    "verify_exp": True
                }
            )
        else:
            # HS256 Fallback
            payload = jwt.decode(
                token, 
                str(SUPABASE_JWT_SECRET), 
                algorithms=["HS256"],  
                options={
                    "verify_aud": False,
                    "verify_iss": False,
                    "verify_sub": True,
                    "verify_exp": True
                }
            )
            
        return payload

    except jwt.ExpiredSignatureError:
        print("❌ JWT Error: Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"❌ JWT Verification Error: {error_type}: {error_msg}")
        print(f"   Token (first 20 chars): {token[:20]}...")
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Session expired or invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_id(claims: dict = Depends(get_current_user_claims)) -> str:
    """Returns the user ID (sub) from valid claims"""
    user_id = claims.get("sub")
    if user_id is None:
        print("❌ JWT Error: No sub in payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user information (sub)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

