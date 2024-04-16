from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from config.db import Base

class Club(Base):
   __tablename__ = 'clubs'
   
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(50), index=True)
   
   players = relationship("Player", back_populates="club")