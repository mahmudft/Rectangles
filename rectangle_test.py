import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from .app import app, get_db, engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Rectangle, Base


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.fixture
def generate_fake_data():
    def _generate_fake_data():
        with TestingSessionLocal() as session:
            rectangles = [
                Rectangle(x1=0.0, y1=0.0, x2=1.0, y2=1.0),
                Rectangle(x1=1.5, y1=1.5, x2=2.5, y2=2.5),
                Rectangle(x1=0.5, y1=0.5, x2=2.0, y2=2.0)
            ]
            session.add_all(rectangles)
            session.commit()
    return _generate_fake_data


@pytest.mark.asyncio
async def test_intersect_segments(generate_fake_data):

    generate_fake_data()
    client = TestClient(app)

    response = client.get("/intersect/?x1=1.0&y1=1.0&x2=2.0&y2=2.0")
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get("/intersect/?x1=3.0&y1=3.0&x2=4.0&y2=4.0")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = client.get("/intersect/?x1=0.5&y1=0.5&x2=1.5&y2=1.5")
    assert response.status_code == 200
    assert len(response.json()) == 2