from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class Club(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str

    players: list["Player"] = Relationship(back_populates="club")
