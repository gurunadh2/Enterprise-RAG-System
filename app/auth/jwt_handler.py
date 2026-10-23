import os
from datetime import datetime
from datetime import timedelta

from jose import JWTError
from jose import jwt

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import (
    OAuth2PasswordBearer
)



SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is required")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def create_access_token(
    username
):

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(
    token
):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):

    credentials_exception = (
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get(
            "sub"
        )

        if username is None:

            raise credentials_exception

        return username

    except JWTError:

        raise credentials_exception