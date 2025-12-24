import os
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
ACCESS_TOKEN_EXPIRE = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

# timedelta(hours=1)
# ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 3))
# ACCESS_TOKEN_EXPIRE = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

# timedelta(days=7)
# ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 7))
# ACCESS_TOKEN_EXPIRE = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)



def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()

    # UTC-aware timestamps (best practice)
    now = datetime.now(timezone.utc)

    # Token expiration from argument or ENV VAR
    expire = now + (expires_delta or ACCESS_TOKEN_EXPIRE)

    # Add issued-at timestamp (important for validation)
    to_encode.update({
        "exp": expire,
        "iat": now, #to prevent replay attack
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_input_token(token: str) -> dict:
    """Verifies JWT access token  & returns decoded payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except InvalidTokenError:
        raise

# def get_current_user(token: str) -> str:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     # Read JWT from secure cookie
#     token = request.cookies.get("access_token")
#     if not token:
#         raise credentials_exception

#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
#         user_id = payload.get("sub")

#         if user_id is None:
#             raise credentials_exception
#         return user_id

#     except JWTError:
#         raise credentials_exception