from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, database
from app.auth import auth_bearer, jwt_handler
from app.models import schemas

database.setup()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["home"])
async def home():
    return {"message": "Welcome to veloking API"}


@app.post("/user/login", tags=["user"])
async def user_login(login_data: schemas.LoginSchema, db: Session = Depends(get_db)):
    user = crud.user_get_by_username(login_data.username, db)
    if user:
        if user.disabled:
            raise HTTPException(status_code=400, detail="User is disabled")
        if database.user_verify(login_data.password, user.password):
            return jwt_handler.encode(user.username)
    raise HTTPException(status_code=400, detail="Incorrect login details")


@app.post("/user/create", tags=["user"])
async def user_create(user: schemas.UserSchema, db: Session = Depends(get_db)):
    if crud.user_get_by_username(user.username, db):
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.user_create(user, db)


@app.get("/user/list", tags=["user"])
async def user_list(db: Session = Depends(get_db)):
    users = crud.user_get_all(db)
    users = [user.fullname for user in users]
    return {"users": users}


@app.get("/user/me", tags=["user"])
async def user_get_myself(
    token: str = Depends(auth_bearer.JWTBearer()), db: Session = Depends(get_db)
):
    payload = jwt_handler.decode(token)
    username = payload["username"]
    user = crud.user_get_by_username(username, db)
    return user


@app.put("/user/point", tags=["user"])
async def user_move_to_point(
    username: str, point_key: str, db: Session = Depends(get_db)
):
    user = crud.user_get_by_username(username, db)
    point = crud.point_get_by_point_key(point_key, db)
    crud.user_move_to_point(user, point, db)


@app.put("/price/create", tags=["price"])
async def price_create(price: schemas.PriceSchema, db: Session = Depends(get_db)):
    crud.price_create(price, db)


@app.post("/point/create", tags=["point"])
async def point_create(point: schemas.PointSchema, db: Session = Depends(get_db)):
    if crud.point_get_by_point_key(point.point_key, db):
        raise HTTPException(status_code=400, detail="Point already registered")
    crud.point_create(point, db)


@app.get("/point/list", tags=["point"])
async def point_list(db: Session = Depends(get_db)):
    points = crud.point_get_all(db)
    points = [
        {
            "point_key": point.point_key,
            "name": point.name,
        }
        for point in points
    ]
    return {"points": points}


# @app.post("/rental/prepayment", tags=["rental"])
# async def rental_calculate_prepayment(
#     prepayment: schemas.PrepaymentSchema, db: Session = Depends(get_db)
# ):
#     return crud.rental_calculate_price(prepayment, db)


@app.get("/vehicle/list", tags=["vehicle"])
async def vehicle_list(db: Session = Depends(get_db)):
    vehicles = crud.vehicle_get_all(db)
    vehicles = [
        {
            "superior_category": vehicle.superior_category,
            "sub_category": vehicle.sub_category,
            "vehicle_key": vehicle.vehicle_key,
            "rented": vehicle.rented,
            "rental_point": vehicle.rental_point.point_key,
        }
        for vehicle in vehicles
    ]
    return {"vehicles": vehicles}


@app.get("/vehicle/move", tags=["vehicle"])
async def vehicle_move(vehicle_key: str, point_key: str, db: Session = Depends(get_db)):
    crud.vehicle_move(vehicle_key, point_key, db)


# @app.post("/rental/create", tags=["rental"])
# async def rental_create(rental: schemas.RentalSchema,
#                         user: tables.User = Depends(user_get_myself),
#                         db: Session = Depends(get_db)):
#     crud.rental_create(user, rental, db)
#
