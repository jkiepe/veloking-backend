from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import tables, schemas, data, setup
from app.database import SessionLocal, crypt
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

setup.setup_database()

app = FastAPI()

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.get("/", tags=["home"])
async def home() -> dict:
    return {"message": "Welcome to veloking API"}

# USER
@app.post("/user/create", tags=["user"], dependencies=[Depends(JWTBearer())])
async def user_create(user: schemas.UserSchema, database: Session = Depends(get_database)):
    if data.user_get_username(username=user.username, database=database):
        raise HTTPException(status_code=400, detail="Username already registered")
    user.password = crypt.hash(user.password)
    data.user_create(user=user, database=database)
    return signJWT(user.username)


@app.post("/user/login", tags=["user"])
async def user_login(login_data: schemas.UserLoginSchema, database: Session = Depends(get_database)):
    user = data.user_get_username(username=login_data.username, database=database)
    if user:
        if crypt.verify(login_data.password, user.password):
            return signJWT(user.username)
    raise HTTPException(status_code=400, detail="Incorrect login details")

