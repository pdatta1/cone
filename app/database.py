
from sqlalchemy.engine import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 


SQLITE_URI = "sqlite:///./shop.db"

engine = create_engine(
    SQLITE_URI, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autoflush=False, 
    autocommit=False, 
    bind=engine
)

Base = declarative_base() 

def get_db(): 

    db = SessionLocal() 
    try: 
        yield db
    finally: 
        db.close() 

