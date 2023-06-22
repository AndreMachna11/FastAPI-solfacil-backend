import os
from fastapi.security.api_key import APIKeyHeader
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
from dotenv import find_dotenv
load_dotenv(find_dotenv())

api_key_header = APIKeyHeader(name="token", auto_error=True)

def authenticate(token: str = Depends(api_key_header)):
    if token != os.getenv('API_STATIC_KEY'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return token

