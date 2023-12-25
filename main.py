import uvicorn
from decouple import config

HOST = str(config("apihost"))
PORT = int(config("apiport"))
RELOAD = bool(config("apireload"))

if __name__ == "__main__":
    uvicorn.run("app.api:app", host=HOST, port=PORT, reload=RELOAD)
