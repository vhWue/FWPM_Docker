from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from routes import club, player
from config.db import SQLModel, engine

app = FastAPI()

app.include_router(club.router, prefix="/clubs", tags=["clubs"])
app.include_router(player.router, prefix="/players", tags=["players"])

SQLModel.metadata.create_all(engine)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def read_root():
    return {"msg": "Hello football lovers :D"}
