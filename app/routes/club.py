from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config.db import get_session
from models.index import Club

club = APIRouter()


@club.get("/clubs", response_model=list[Club])
async def get_clubs(db: Session = Depends(get_session)):
    clubs = db.query(Club).all()
    return clubs


@club.post("/clubs", response_model=Club)
async def create_club(club: Club, db: Session = Depends(get_session)):
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


@club.put("/clubs/{id}")
async def update_club(id: int, name: str = None, db: Session = Depends(get_session)):
    try:
        club = db.query(Club).filter(Club.id == id).first()

        if club and name:
            club.name = name
            db.commit()

        return JSONResponse(content={"msg": "Club updated"})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status. HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Update_Failed: {e}")


@club.delete("/clubs/{id}")
async def delete_club(id: int, db: Session = Depends(get_session)):
    try:
        club = db.query(Club).filter_by(id=id).first()
        players = club.players

        if club and not players:
            db.delete(club)
            db.commit()
            return JSONResponse(content={"msg": "Club deleted"})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Club not found or still associated!")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Delete_Failed: {e}")
