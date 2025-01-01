from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

# Create PostgreSQL engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLite engine for iMessage database (read-only)
imessage_engine = create_engine(f"sqlite:///{settings.IMESSAGE_DB_PATH}", 
                              connect_args={"check_same_thread": False})
IMSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=imessage_engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get iMessage DB session
def get_imessage_db():
    db = IMSessionLocal()
    try:
        yield db
    finally:
        db.close()