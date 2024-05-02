from fastapi import Depends, HTTPException, Session, status
from sqlmodel import select

from app.models.club import Club, ClubUpdate

async def get_clubs(db: Session, offset: int = 0, limit: int = 20):
    return db.exec(select(Club).offset(offset).limit(limit)).all()


async def get_club(db: Session, club_id: int):
    return db.get(Club, club_id)


async def create_club(db: Session, club: Club):
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


async def update_club(db: Session, db_club: Club, club: ClubUpdate):
    try:
        db_club.sqlmodel_update(club.model_dump(exclude_unset=False))
        db.add(db_club)
        db.commit()
        db.refresh(db_club)
        return db_club
    except Exception as e:
        db.rollback()
        raise e


async def delete_club(db: Session, club: Club):
    try:
        db.delete(club)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e