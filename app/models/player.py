from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship

from config.db import Base

class Player(Base):
   __tablename__ = 'players'
   
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(50), index=True)
   club_id = Column(Integer, ForeignKey("clubs.id"))
   
   club = relationship("Club", back_populates="players")
