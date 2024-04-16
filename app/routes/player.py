from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from models.index import Player, Club

player = APIRouter()
session = SessionLocal()

@player.get("/players")
async def get_players():
   players = session.query(Player).all()
   if not players: 
      return JSONResponse(content={"msg": "No Players"}, status_code=status.HTTP_404_NOT_FOUND)
   return players


@player.post("/player")
async def create_player(name:str, club_id:int):
   
   if name and session.query(Club).filter(Club.id == club_id).first():
      new_player = Player(
         name = name,
         club_id = club_id
      )
      session.add(new_player)
      session.commit()
      return JSONResponse(content={"msg":"Player updated"})
   else:
      return JSONResponse(content={"msg":"Missing/Wrong arguments"}, status_code=status.HTTP_406_NOT_ACCEPTABLE)

@player.put("/player/{id}")
async def update_player(id:int, name:str = None, club_id:int = None):
   try:
      player = session.query(Player).filter(Player.id == id).first()
      
      if player:
         if name:
            player.name = name
         if club_id:
            player.club_id = club_id
         session.commit()
   
      return player
   
   except Exception as e:
      session.rollback()
      response = {"Update_Failed": e}
      return JSONResponse(content = response, status_code = status.HTTP_418_IM_A_TEAPOT)
   
@player.delete("/player/{id}")
async def delete_player(id:int):
   try:
      player = session.query(Player).filter(Player.id == id).first()
      
      if player:
         session.delete(player)
         session.commit()
         return JSONResponse(content={"msg":"Player deleted"})
      else:
         return JSONResponse(content={"msg":"Player not found!"})
      
   except Exception as e:
      session.rollback()
      response = {"Delete_Failed": e}
      return JSONResponse(content = response, status_code = status.HTTP_418_IM_A_TEAPOT)