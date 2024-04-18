from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config.db import get_db
from models.index import Club

club = APIRouter()


@club.get("/clubs")
async def get_clubs(db: Session = Depends(get_db)):
    clubs = db.query(Club).all()
    if not clubs:
        return JSONResponse(content={"msg": "No clubs"}, status_code=status.HTTP_404_NOT_FOUND)
    return clubs


@club.post("/club")
async def create_club(name: str, db: Session = Depends(get_db)):
    if name:
        new_club = Club(
            name=name
        )
        db.add(new_club)
        db.commit()
        return db.query(Club).filter(Club.name == new_club.name).first()
    else:
        return JSONResponse(content={"msg": "Missing/Wrong arguments"},
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)


@club.put("/club/{id}")
async def update_club(id: int, name: str = None, db: Session = Depends(get_db)):
    try:
        club = db.query(Club).filter(Club.id == id).first()

        if club and name:
            club.name = name
            db.commit()

        return JSONResponse(content={"msg": "Club updated"})

    except Exception as e:
        db.rollback()
        return JSONResponse(content={"Update_Failed": e}, status_code=status.HTTP_418_IM_A_TEAPOT)


@club.delete("/club/{id}")
async def delete_club(id: int, db: Session = Depends(get_db)):
    try:
        club = db.query(Club).filter_by(id=id).first()
        players = club.players

        if club and not players:
            db.delete(club)
            db.commit()
            return JSONResponse(content={"msg": "Club deleted"})
        else:
            return JSONResponse(content={"msg": "Club not found or still associated!"})

    except Exception as e:
        db.rollback()
        response = {"Delete_Failed": e}
        return JSONResponse(content=response, status_code=status.HTTP_418_IM_A_TEAPOT)
