from sqlmodel import Session, create_engine, SQLModel
import os

DB_USER = 'root'
DB_PASSWORD = os.getenv('DB_PW') or 'pwroot'
DB_HOSTNAME = os.getenv('DB_HOST') or 'mariadb'
DB_NAME = 'fuba'

URL_DATABASE = "sqlite:///devfuba.db" if os.getenv('APP_ENV') == 'dev' else f'mariadb+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'

engine = create_engine(URL_DATABASE, echo=True, pool_recycle=3600)

def get_session():
    with Session(engine) as session:
        yield session
