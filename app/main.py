from fastapi import FastAPI

from .routers.club import router as club_router

app = FastAPI()

app.include_router(club_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
