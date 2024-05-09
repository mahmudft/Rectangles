from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Rectangle(Base):
    __tablename__ = "rectangles"

    id = Column(Integer, primary_key=True, index=True)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
