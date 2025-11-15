import random
import string
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Optional

import jwt
from fastapi import HTTPException

from ..settings import env_settings

ALPHABET: str = string.ascii_letters


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 1  # 1 hour

def generate_salt() -> str:
    chars:list[str] =[]
    for _ in range(16):
        chars.append(random.choice(ALPHABET))

    return "".join(chars)

def create_access_token(data: dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
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
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def detemenistic_hash(data: str) -> str:
    encoded: bytes = data.encode('utf-8')
    return sha256(encoded).hexdigest()