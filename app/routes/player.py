from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.db import get_db
from models.index import Player, Club

player = APIRouter()


@player.get("/players")
async def get_players(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    if not players:
        return JSONResponse(content={"msg": "No Players"}, status_code=status.HTTP_404_NOT_FOUND)
    return players


@player.post("/player")
async def create_player(name: str, club_id: int, db: Session = Depends(get_db)):
    if name and db.query(Club).filter(Club.id == club_id).first():
        new_player = Player(
            name=name,
            club_id=club_id
        )
        db.add(new_player)
        db.commit()
        return JSONResponse(content={"msg": "Player updated"})
    else:
        return JSONResponse(content={"msg": "Missing/Wrong arguments"},
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)


@player.put("/player/{id}")
async def update_player(id: int, name: str = None, club_id: int = None, db: Session = Depends(get_db)):
    try:
        player = db.query(Player).filter(Player.id == id).first()

        if player:
            if name:
                player.name = name
            if club_id:
                player.club_id = club_id
            db.commit()

        return player

    except Exception as e:
        db.rollback()
        response = {"Update_Failed": e}
        return JSONResponse(content=response, status_code=status.HTTP_418_IM_A_TEAPOT)


@player.delete("/player/{id}")
async def delete_player(id: int, db: Session = Depends(get_db)):
    try:
        player = db.query(Player).filter(Player.id == id).first()

        if player:
            db.delete(player)
            db.commit()
            return JSONResponse(content={"msg": "Player deleted"})
        else:
            return JSONResponse(content={"msg": "Player not found!"})

    except Exception as e:
        db.rollback()
        response = {"Delete_Failed": e}
        return JSONResponse(content=response, status_code=status.HTTP_418_IM_A_TEAPOT)
