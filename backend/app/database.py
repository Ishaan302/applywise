from sqlalchemy import create_engine, MetaData # creates a SQLAlchemy Engine.
from sqlalchemy.orm import sessionmaker, declarative_base # (sessionmaker creates session ,talks through engine ->postgresql), (declarativebase creates the base class that SQLAlchemy models will inherit from.)   
import os
from dotenv import load_dotenv   # It allows Python to read var from a .env file.

load_dotenv()  # Read the .env file and load its var into the environment.

DATABASE_URL = os.getenv("DATABASE_URL")  # python retrieve var from env file

engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base() # creates base class for database models.

def get_db():  # provides database session to fastapi routes
    db = sessionlocal() #  A new database session is created.
    try:           # --|it means Give this database session to whoever needs it,
        yield db   # --|but make sure the cleanup happens afterward.
    
    finally:       #--|Regardless of whether route succeeds or throws an exception
        db.close() #--|the database session gets closed
