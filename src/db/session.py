from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.config.app_config import settings

engine = create_engine(settings.DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session