from .settings import env_settings

import random 

from fastapi import HTTPException
from fastapi.security import HTTPBearer
import jwt

from datetime import datetime, timedelta, UTC
from typing import Optional
from hashlib import sha256

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 1  # 1 hour

async def generate_salt() -> str:
    chars:list[str] =[]
    for _ in range(16):
        chars.append(random.choice(ALPHABET))

    return "".join(chars)

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "iat": datetime.now(UTC)})

    return jwt.encode(to_encode, env_settings.SECRET_KEY, algorithm=env_settings.ALGORITHM)

def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, env_settings.SECRET_KEY, algorithms=[env_settings.ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user_id
    except jwt.ExpiredSignatureError:
        return HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def detemenistic_hash(data: str) -> str:
    data = data.encode('utf-8')
    return sha256(data).hexdigest()