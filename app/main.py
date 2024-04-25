from fastapi import FastAPI

from routes import club, player
from config.db import SQLModel, engine

app = FastAPI()

app.include_router(club.router, prefix="/clubs", tags=["clubs"])
app.include_router(player.router, prefix="/players", tags=["players"])

SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"msg": "Hello football lovers :D"}
