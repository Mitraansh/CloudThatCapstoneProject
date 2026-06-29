import hashlib
import hmac
import os
from typing import Optional

from fastapi import HTTPException

SECRET_KEY = os.getenv("APP_SECRET_KEY", "default-secret")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(password), password_hash)


def create_token(email: str) -> str:
    return hmac.new(SECRET_KEY.encode("utf-8"), email.encode("utf-8"), "sha256").hexdigest()


def get_email_from_token(token: str, email: str) -> bool:
    expected = create_token(email)
    return hmac.compare_digest(expected, token)


def validate_login(email: str, password: str, stored_hash: str) -> bool:
    if not password:
        return False
    return verify_password(password, stored_hash)
