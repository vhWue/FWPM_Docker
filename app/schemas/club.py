from pydantic import BaseModel


class ClubBase(BaseModel):
    name: str


class Club(ClubBase):
    name: str

    class Config:
        orm_mode = True
