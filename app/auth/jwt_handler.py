import time
import jwt
from decouple import config

SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")
EXPIRE_MINUTES = int(config("expire"))


def encode(username: str):
    payload = {
        "username": username,
        "expires": time.time() + EXPIRE_MINUTES * 60
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


def decode(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

