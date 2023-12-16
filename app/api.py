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

# , dependencies=[Depends(JWTBearer())]
# USER
@app.post("/user/create", tags=["user"])
async def user_create(user: schemas.UserSchema,
                      database: Session = Depends(get_database)):
    if data.user_get_by_username(user.username, database):
        raise HTTPException(status_code=400, detail="Username already registered")
    user.password = crypt.hash(user.password)
    data.user_create(user, database)
    return signJWT(user.username)


@app.post("/user/login", tags=["user"])
async def user_login(login_data: schemas.UserLoginSchema,
                     database: Session = Depends(get_database)):
    user = data.user_get_by_username(login_data.username, database)
    if user:
        if crypt.verify(login_data.password, user.password):
            return signJWT(user.username)
    raise HTTPException(status_code=400, detail="Incorrect login details")


@app.put("/user/point", tags=["user"])
async def user_move_to_point(username: str,
                             key: str,
                             database: Session = Depends(get_database)):
    user = data.user_get_by_username(username, database)
    point = data.point_get_by_key(point_key, database)
    data.user_move_to_point(user, point, database)


# POINT
@app.get("/point/users", tags=["point"])
async def point_get_users(key: str,
                          database: Session = Depends(get_database)):
    point = data.point_get_by_key(key, database)
    return {user.username:user.role for user in point.users}


@app.post("/point/create", tags=["point"])
async def point_create(point: schemas.PointSchema,
                       database: Session = Depends(get_database)):
    if data.point_get_by_key(point.key, database):
        raise HTTPException(status_code=400, detail="Point already registered")
    data.point_create(point=point, database=database)

