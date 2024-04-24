from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class ClubBase(SQLModel):
    name: str


class ClubUpdate(ClubBase):
    pass


class Club(ClubBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    players: list["Player"] = Relationship(back_populates="club")
