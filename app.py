from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Rectangle, Base

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/intersect/")
async def intersect_segments(x1: float, y1: float, x2: float, y2: float, db: Session = Depends(get_db), response_model=None):
    intersecting_rectangles = db.query(Rectangle).filter(
        (x1 <= Rectangle.x2) & (x2 >= Rectangle.x1) &
        (y1 <= Rectangle.y2) & (y2 >= Rectangle.y1)
    ).all()
    return intersecting_rectangles
