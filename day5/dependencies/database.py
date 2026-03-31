from config import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# replace with your credentials
DATABASE_URL = URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()