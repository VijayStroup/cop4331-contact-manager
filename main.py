from db import db
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import api, pages

db.init()

app = FastAPI()
app.include_router(api.router)
app.include_router(pages.router)
app.mount('/static', StaticFiles(directory='static'), name='static')
