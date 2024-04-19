from sqlmodel import Session, create_engine, SQLModel

DB_USER = 'root'
DB_PASSWORD = 'pwroot'
DB_HOSTNAME = 'mariadb'
DB_NAME = 'fuba'
URL_DATABASE = f'mariadb+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'

engine = create_engine(URL_DATABASE, echo=True, pool_recycle=3600)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
