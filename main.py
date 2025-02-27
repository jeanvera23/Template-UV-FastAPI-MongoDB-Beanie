from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from api.middlewares.errorHandling import ErrorHandlingMiddleware
import logging

from api.routes.base import api_router
from utils import database
# creating the FastAPI app

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connectToDatabase()
    yield
    await database.closeDatabaseConnection()

app = FastAPI(lifespan=lifespan)

# logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="logs/log.txt", level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s]: %(message)s", filemode="w")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandlingMiddleware)

app.include_router(api_router)

@app.get("/", tags=["Application Details"])
async def system():

    logger.info("logging from the root logger")
    return {
        "name": "APP Name",
        "version": "0.0.1",
        "description": "Application description"
    }