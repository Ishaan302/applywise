import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://ishaan:secret@localhost:5432/applywise_test"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    client.post("/auth/register", json={"email": "test@test.com", "password": "test1234"})
    r = client.post("/auth/login", data={"username": "test@test.com", "password": "test1234"})
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}