import sys
import os
from pathlib import Path

# Loyiha ildizini qo'shish
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test uchun alohida database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Har bir test oldidan jadvalarni yaratish
@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Har bir test oldidan bazani tozalab, qayta yaratadi"""
    Base.metadata.drop_all(bind=engine)  # Eski ma'lumotlarni tozalash
    Base.metadata.create_all(bind=engine)  # Jadvalarni yaratish
    yield
    # Test tugagandan keyin ham tozalash mumkin (ixtiyoriy)
    # Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ====================== TESTS ======================


def test_create_customer():
    response = client.post(
        "/api/customers",
        json={
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+998901234567",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Customer"
    assert "id" in data


def test_list_customers():
    response = client.get("/api/customers")
    assert response.status_code == 200


def test_dashboard_stats():
    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_customers" in data
    assert "pipeline_value" in data
