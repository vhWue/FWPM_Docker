from fastapi import FastAPI
from routes.index import player, club
from config.db import Base, engine

#Create the tables according to the models (SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(player)
app.include_router(club)

@app.get("/")
def read_root():
   return {"msg": "Hello football lovers :D"}