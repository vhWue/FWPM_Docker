from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class Player(PlayerBase):
    name: str
    club_id: int

    class Config:
        orm_mode = True
