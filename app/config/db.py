from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USER = 'root'
DB_PASSWORD = 'pwroot'
DB_HOSTNAME = 'mariadb'
DB_NAME = 'fuba'
URL_DATABASE = f'mariadb+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:3306/{DB_NAME}'

engine = create_engine(URL_DATABASE, echo=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()