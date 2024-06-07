from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging

from src.routers import pods

app = FastAPI()


logging.basicConfig(
    filename="api_log.log",
    filemode="a",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

app.include_router(router=pods.router)


@app.get("/", response_class=HTMLResponse)
async def main():
    return "Welcome to kubernetes dashboard"