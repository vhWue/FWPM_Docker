from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#URL_DATABASE='mariadb+pymysql://root:root@localhost:3306/testdb'
URL_DATABASE='sqlite:///fuba.db'

engine = create_engine(URL_DATABASE, echo=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()