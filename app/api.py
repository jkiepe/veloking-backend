from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import tables, schemas, data, database
from .auth import auth_bearer, jwt_handler


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


database.setup()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["home"])
async def home() -> dict:
    return {"message": "Welcome to veloking API"}


@app.post("/user/login", tags=["user"])
async def user_login(login_data: schemas.LoginSchema,
                     db: Session = Depends(get_db)):
    user = data.user_get_by_username(login_data.username, db)
    if user:
        if user.disabled:
            raise HTTPException(status_code=400, detail="User is disabled")
        if database.crypt.verify(login_data.password, user.password):
            return jwt_handler.encode(user.username)
    raise HTTPException(status_code=400, detail="Incorrect login details")


@app.post("/user/create", tags=["user"])
async def user_create(user: schemas.UserSchema,
                      db: Session = Depends(get_db)):
    if data.user_get_by_username(user.username, db):
        raise HTTPException(status_code=400, detail="Username already registered")
    user.password = database.crypt.hash(user.password)
    data.user_create(user, db)


@app.get("/user/list", tags=["user"])
async def user_list(db: Session = Depends(get_db)):
    users = data.user_get_all(db)
    users = [user.fullname for user in users]
    return {"users": users}


@app.get("/user/me", tags=["user"])
async def user_get_myself(token: str = Depends(auth_bearer.JWTBearer()),
                          db: Session = Depends(get_db)):
    payload = jwt_handler.decode(token)
    username = payload["username"]
    user = data.user_get_by_username(username, db)
    return user


@app.put("/user/point", tags=["user"])
async def user_move_to_point(username: str,
                             key: str,
                             db: Session = Depends(get_db)):
    user = data.user_get_by_username(username, db)
    point = data.point_get_by_key(point_key, db)
    data.user_move_to_point(user, point, db)


# @app.get("/point/users", tags=["point"])
# async def point_get_users(key: str,
#                           db: Session = Depends(get_db)):
#     point = data.point_get_by_key(key, db)
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
                       db: Session = Depends(get_db)):
    if data.point_get_by_key(point.key, db):
        raise HTTPException(status_code=400, detail="Point already registered")
    data.point_create(point, db)



@app.get("/point/list", tags=["point"])
async def point_list(db: Session = Depends(get_db)):
    points = data.point_get_all(db)
    points = [{
        "id": point.id,
        "key": point.key,
       "name": point.name,
       } for point in points]
    return {"points": points}


@app.post("/rental/create", tags=["rental"])
async def rental_create(rental: schemas.RentalSchema,
                        user: tables.User = Depends(user_get_myself),
                        db: Session = Depends(get_db)):
    data.rental_create(user, rental, db)

