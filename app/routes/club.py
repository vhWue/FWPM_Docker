from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config.db import get_db
from models.index import Club

club = APIRouter()


@club.get("/clubs")
async def get_clubs(db: Session = Depends(get_db)):
    clubs = db.query(Club).all()
    return clubs


@club.post("/clubs")
async def create_club(name: str, db: Session = Depends(get_db)):
    if name:
        new_club = Club(
            name=name
        )
        db.add(new_club)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Missing/Wrong arguments")


@club.put("/clubs/{id}")
async def update_club(id: int, name: str = None, db: Session = Depends(get_db)):
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
async def delete_club(id: int, db: Session = Depends(get_db)):
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
