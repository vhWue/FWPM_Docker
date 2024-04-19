from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from models.index import Club


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True)

    club_id: Optional[int] = Field(default=None, foreign_key="club.id")
    club: Optional[Club] = Relationship(back_populates="players")
