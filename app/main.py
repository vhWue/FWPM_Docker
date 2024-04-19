from fastapi import FastAPI

from routes.index import player, club

app = FastAPI()

app.include_router(player)
app.include_router(club)

@app.get("/")
def read_root():
   return {"msg": "Hello football lovers :D"}