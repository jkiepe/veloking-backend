import uvicorn
from decouple import config

HOST = config("apihost")
PORT = config("apiport")

if __name__ == "__main__":
    uvicorn.run("app.api:app", host=HOST, port=PORT, reload=True)
