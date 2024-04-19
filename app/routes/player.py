from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config.db import get_session
from models.index import Player

player = APIRouter()


@player.get("/players", response_model=list[Player])
async def get_players(db: Session = Depends(get_session)):
    players = db.query(Player).all()
    return players


@player.get("/player/{id}", response_model=Player)
async def get_player(id: int, db: Session = Depends(get_session)):
    player = db.get(Player, id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player


@player.post("/players")
async def create_player(player: Player, db: Session = Depends(get_session)):
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@player.put("/players/{id}")
async def update_player(id: int, name: str = None, club_id: int = None,
                        db: Session = Depends(get_session)):
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
async def delete_player(id: int, db: Session = Depends(get_session)):
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
