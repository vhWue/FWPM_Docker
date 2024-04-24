from fastapi import FastAPI

from routes import club, player

app = FastAPI()

app.include_router(club.router, prefix="/clubs", tags=["clubs"])
app.include_router(player.router, prefix="/players", tags=["players"])


@app.get("/")
def read_root():
    return {"msg": "Hello football lovers :D"}
