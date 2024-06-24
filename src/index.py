from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import logging

from fastapi.staticfiles import StaticFiles

from src.routers import pods, deployments, cluster
from src.routers.pods import templates

app = FastAPI()

logging.basicConfig(
    filename="api_log.log",
    filemode="a",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

app.include_router(router=pods.router)
app.include_router(router=deployments.router)
app.include_router(router=cluster.router)
app.mount("/static", StaticFiles(directory="src/static"), name='static')

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")