from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from etl import settings

engine = create_engine(settings.DATABASE)

session_factory = sessionmaker()
session_factory.configure(bind=engine)
session = session_factory()


