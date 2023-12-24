from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import tables, schemas, data, setup
from .database import SessionLocal, crypt
from .auth import auth_bearer, jwt_handler

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

setup.setup_database()

@app.get("/", tags=["home"])
async def home() -> dict:
    return {"message": "Welcome to veloking API"}


@app.post("/user/login", tags=["user"])
async def user_login(login_data: schemas.LoginSchema,
                     database: Session = Depends(get_database)):
    user = data.user_get_by_username(login_data.username, database)
    if user:
        if user.disabled:
            raise HTTPException(status_code=400, detail="User is disabled")
        if crypt.verify(login_data.password, user.password):
            return jwt_handler.encode(user.username)
    raise HTTPException(status_code=400, detail="Incorrect login details")


@app.post("/user/create", tags=["user"])
async def user_create(user: schemas.UserSchema,
                      database: Session = Depends(get_database)):
    if data.user_get_by_username(user.username, database):
        raise HTTPException(status_code=400, detail="Username already registered")
    user.password = crypt.hash(user.password)
    data.user_create(user, database)


@app.get("/user/list", tags=["user"])
async def user_list(database: Session = Depends(get_database)):
    users = data.user_get_all(database)
    users = [user.fullname for user in users]
    return {"users": users}


@app.get("/user/me", tags=["user"])
async def user_get_myself(token: str = Depends(auth_bearer.JWTBearer()),
                          database: Session = Depends(get_database)):
    payload = jwt_handler.decode(token)
    username = payload["username"]
    user = data.user_get_by_username(username, database)
    return user


# @app.put("/user/point", tags=["user"])
# async def user_move_to_point(username: str,
#                              key: str,
#                              database: Session = Depends(get_database)):
#     user = data.user_get_by_username(username, database)
#     point = data.point_get_by_key(point_key, database)
#     data.user_move_to_point(user, point, database)


# @app.get("/point/users", tags=["point"])
# async def point_get_users(key: str,
#                           database: Session = Depends(get_database)):
#     point = data.point_get_by_key(key, database)
#     return {
#         user.username:{
#             "username": user.username, 
#             "fullname":user.fullname, 
#             "role":user.role
#         }
#         for user in point.users
#     }


@app.post("/point/create", tags=["point"])
async def point_create(point: schemas.PointSchema,
                       database: Session = Depends(get_database)):
    if data.point_get_by_key(point.key, database):
        raise HTTPException(status_code=400, detail="Point already registered")
    data.point_create(point, database)



@app.get("/point/list", tags=["point"])
async def point_list(database: Session = Depends(get_database)):
    points = data.point_get_all(database)
    points = [point.name for point in points]
    return {"points": points}


@app.post("/rental/create", tags=["rental"])
async def rental_create(rental: schemas.RentalSchema,
                        user: tables.User = Depends(user_get_myself),
                        database: Session = Depends(get_database)):
    data.rental_create(user, rental, database)

