import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verifies the JWT token from Supabase and returns the user ID (sub).
    Uses HS256 algorithm with SUPABASE_JWT_SECRET.
    """
    token = credentials.credentials
    
    if not SUPABASE_JWT_SECRET:
        print("CRITICAL: SUPABASE_JWT_SECRET is not set!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server authentication configuration error",
        )
    
    try:
        # Decode JWT using HS256 algorithm
        payload = jwt.decode(
            token, 
            str(SUPABASE_JWT_SECRET), 
            algorithms=["HS256"], 
            options={
                "verify_aud": False,
                "verify_iss": False,
                "verify_sub": True,
                "verify_exp": True  # Verify expiration
            }
        )
        
        user_id = payload.get("sub")
        if user_id is None:
            print("JWT Error: No sub in payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user information (sub)",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_id
        
    except JWTError as e:
        print(f"JWT Verification Error: {str(e)}")
        print(f"Token (first 20 chars): {token[:20]}...")
        print(f"JWT Secret (first 10 chars): {str(SUPABASE_JWT_SECRET)[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Session expired or invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
