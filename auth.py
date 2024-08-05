# auth.py
from fastapi import Header, HTTPException
from typing import Optional

from config import STATIC_TOKEN


# Define the static token for authentication


def get_token_header(x_token: Optional[str] = Header(None)) -> str:
    if x_token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return x_token
