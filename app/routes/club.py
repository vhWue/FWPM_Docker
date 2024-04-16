from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from models.index import Club, Player

club = APIRouter()
session = SessionLocal()

@club.get("/clubs")
async def get_clubs():
   clubs = session.query(Club).all()
   if not clubs: 
      return JSONResponse(content={"msg": "No clubs"}, status_code=status.HTTP_404_NOT_FOUND)
   return clubs


@club.post("/club")
async def create_club(name:str):
   if name:
      new_club = Club(
         name = name
      )
      session.add(new_club)
      session.commit()
      return session.query(Club).filter(Club.name == new_club.name).first()
   else:
      return JSONResponse(content={"msg":"Missing/Wrong arguments"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)

@club.put("/club/{id}")
async def update_club(id:int , name:str = None):
   try:
      club = session.query(Club).filter(Club.id == id).first()
      
      if club and name:
         club.name = name
         session.commit()
      
      return JSONResponse(content={"msg":"Club updated"})
   
   except Exception as e:
      session.rollback()
      return JSONResponse(content = {"Update_Failed": e}, status_code = status.HTTP_418_IM_A_TEAPOT) 

@club.delete("/club/{id}")
async def delete_club(id:int):
   try:
      club = session.query(Club).filter_by(id = id).first()
      players = club.players
      
      if club and not players:
         session.delete(club)
         session.commit()
         return JSONResponse(content={"msg":"Club deleted"})
      else:
         return JSONResponse(content={"msg":"Club not found or still associated!"})
   
   except Exception as e:
      session.rollback()
      response = {"Delete_Failed": e}
      return JSONResponse(content = response, status_code = status.HTTP_418_IM_A_TEAPOT)