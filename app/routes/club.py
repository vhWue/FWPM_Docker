from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from config.db import get_session
from models.club import Club, ClubUpdate

router = APIRouter()


@router.get("/", response_model=list[Club])
async def get_clubs(offset: int = 0, limit: int = 20, db: Session = Depends(get_session)):
    clubs = db.exec(select(Club).offset(offset).limit(limit)).all()
    return clubs


@router.get("/{club_id}", response_model=Club)
async def get_club(club_id: int, db: Session = Depends(get_session)):
    club = db.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")
    return club


@router.post("/", response_model=Club)
async def create_club(club: Club, db: Session = Depends(get_session)):
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


@router.put("/{club_id}")
async def update_club(club_id: int, club: ClubUpdate, db: Session = Depends(get_session)):
    db_club = db.get(Club, club_id)
    if not db_club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

    try:
        db_club.sqlmodel_update(club.model_dump(exclude_unset=False))
        db.add(db_club)
        db.commit()
        db.refresh(db_club)
        return db_club
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Update_Failed: {e}")


@router.delete("/{club_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_club(club_id: int, db: Session = Depends(get_session)):
    club = db.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")

    players = club.players
    if not len(players) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Club still has associated players!")
    try:
        db.delete(club)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Delete_Failed: {e}")
