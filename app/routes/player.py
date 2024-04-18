
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.db import get_db
from models.index import Player, Club

player = APIRouter()


@player.get("/players")
async def get_players(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    return players

@player.get("/player/{id}")
async def get_player(id: int, db: Session = Depends(get_db)):
    player_found = db.query(Player).filter(Player.id == id).first()
    if not player_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player_found

@player.post("/players")
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
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Missing/Wrong arguments")


@player.put("/players/{id}")
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Update failed: {e}")


@player.delete("/players/{id}")
async def delete_player(id: int, db: Session = Depends(get_db)):
    try:
        player = db.query(Player).filter(Player.id == id).first()

        if player:
            db.delete(player)
            db.commit()
            return JSONResponse(content={"msg": "Player deleted"})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Player not found")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Delete failed: {e}")
