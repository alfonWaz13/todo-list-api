import uvicorn
from fastapi import FastAPI

from source.database import engine
from source.models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
