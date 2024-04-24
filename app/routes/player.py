from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from config.db import get_session
from models.club import Club
from models.player import Player, PlayerUpdate

router = APIRouter()


@router.get("/", response_model=list[Player])
async def get_players(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    players = db.exec(select(Player).offset(offset).limit(limit)).all()
    return players


@router.get("/{player_id}", response_model=Player)
async def get_player(player_id: int, db: Session = Depends(get_session)):
    player = db.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player


@router.post("/", response_model=Player)
async def create_player(player: Player, db: Session = Depends(get_session)):
    db_club = db.get(Club, player.club_id)
    if not db_club:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Club specified for player not found")
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@router.put("/{player_id}", response_model=Player)
async def update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_session)):
    db_player = db.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

    db_club = db.get(Club, player.club_id)
    if not db_club:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Club specified for player not found")

    try:
        db_player.sqlmodel_update(player.model_dump(exclude_unset=False))
        db.add(db_player)
        db.commit()
        db.refresh(db_player)
        return db_player
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Update failed: {e}")


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int, db: Session = Depends(get_session)):
    player = db.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")

    try:
        db.delete(player)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Delete failed: {e}")
