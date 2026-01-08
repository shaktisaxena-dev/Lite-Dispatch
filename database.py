from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
# We get the URL from the environment, or default to localhost for dev
# NOTE: When running locally with Docker DB, we use localhost.
# Inside Docker (if we ran the app there), we would use 'db'.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dispatch:dispatch@localhost:5432/dispatch")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()