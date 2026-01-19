import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import json

security = HTTPBearer()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

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
        # Check for placeholder secret and skip verification if so
        if str(SUPABASE_JWT_SECRET) == "your-jwt-secret-here":
            print("⚠️ WARNING: Using placeholder JWT secret. Skipping signature verification!")
            payload = jwt.decode(
                token, 
                "", 
                options={
                    "verify_signature": False,
                    "verify_aud": False,
                    "verify_iss": False,
                    "verify_sub": True,
                    "verify_exp": True
                }
            )
        else:
            # Decode JWT - support both HS256 (old Supabase) and ES256 (new Supabase)
            payload = jwt.decode(
                token, 
                str(SUPABASE_JWT_SECRET), 
                algorithms=["HS256", "ES256"],  # Support both algorithms
                options={
                    "verify_aud": False,
                    "verify_iss": False,
                    "verify_sub": True,
                    "verify_exp": True  # Verify expiration
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
        # Try to decode header to see the algorithm
        try:
            header = json.loads(jwt.get_unverified_header(token))
            print(f"   Token algorithm: {header.get('alg', 'unknown')}")
        except:
            pass
            
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

