import jwt
from datetime import datetime, timedelta

SECRET = "Pass1234"
ALGORITHM = "HS256"
EXP_MINUTES = 60

def create_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=EXP_MINUTES)
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload["id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None