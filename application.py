from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from routers import todos
from source.database import engine
from source.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI()
app.include_router(todos.router)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
