from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import api, pages

app = FastAPI()
app.include_router(api)
app.include_router(pages)
app.mount('/static', StaticFiles(directory='static'), name='static')
