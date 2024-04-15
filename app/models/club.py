from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    # Add more columns as needed
