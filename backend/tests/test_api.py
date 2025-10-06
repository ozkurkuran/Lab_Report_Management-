"""
Pytest tests for Lab Report API
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models import User, Project, Experiment, Entry


# Test veritabanı
@pytest.fixture(name="session")
def session_fixture():
    """Test için in-memory SQLite veritabanı"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Test client"""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session):
    """Test kullanıcısı"""
    user = User(
        name="Test User",
        email="test@example.com",
        role="researcher"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_project")
def test_project_fixture(session: Session, test_user: User):
    """Test projesi"""
    project = Project(
        name="YBCO Test Project",
        description="Test superconductor project",
        tags=["YBCO", "test"],
        created_by=test_user.id,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


def test_read_root(client: TestClient):
    """Root endpoint testi"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


def test_health_check(client: TestClient):
    """Health check testi"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_project(client: TestClient, test_user: User):
    """Proje oluşturma testi"""
    response = client.post(
        "/api/projects/",
        json={
            "name": "New Test Project",
            "description": "Testing project creation",
            "tags": ["test", "api"],
            "created_by": test_user.id,
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Test Project"
    assert "id" in data
    assert data["tags"] == ["test", "api"]


def test_list_projects(client: TestClient, test_project: Project):
    """Proje listeleme testi"""
    response = client.get("/api/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == test_project.name


def test_get_project(client: TestClient, test_project: Project):
    """Proje detay testi"""
    response = client.get(f"/api/projects/{test_project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_project.id
    assert data["name"] == test_project.name


def test_create_experiment(client: TestClient, test_user: User, test_project: Project):
    """Deney oluşturma testi"""
    response = client.post(
        f"/api/experiments/?user_id={test_user.id}",
        json={
            "project_id": test_project.id,
            "title": "VDP Measurement",
            "description": "Van der Pauw measurement at 77K",
            "tags": ["VDP", "77K"],
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "VDP Measurement"
    assert data["project_id"] == test_project.id


def test_create_entry(client: TestClient, session: Session, test_user: User, test_project: Project):
    """Entry oluşturma testi"""
    # Önce bir deney oluştur
    experiment = Experiment(
        project_id=test_project.id,
        title="Test Experiment",
        tags=["test"]
    )
    session.add(experiment)
    session.commit()
    session.refresh(experiment)
    
    # Entry oluştur
    response = client.post(
        "/api/entries/",
        json={
            "experiment_id": experiment.id,
            "author_id": test_user.id,
            "title": "Günlük-2025-10-06",
            "body_md": "## Deney Koşulları\n- T=77K\n- B=0.5T",
            "tags": ["YBCO", "VDP"],
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Günlük-2025-10-06"
    assert data["version"] == 1


def test_update_entry_creates_new_version(client: TestClient, session: Session, test_user: User, test_project: Project):
    """Entry güncelleme versiyonlama testi"""
    # Deney ve entry oluştur
    experiment = Experiment(
        project_id=test_project.id,
        title="Test Experiment",
        tags=["test"]
    )
    session.add(experiment)
    session.commit()
    session.refresh(experiment)
    
    entry = Entry(
        experiment_id=experiment.id,
        author_id=test_user.id,
        title="Original Title",
        body_md="Original content",
        tags=[]
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    
    # Entry'yi güncelle
    response = client.patch(
        f"/api/entries/{entry.id}",
        json={
            "title": "Updated Title",
            "body_md": "Updated content",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["version"] == 2
    assert data["parent_version_id"] == entry.id


def test_list_entries_with_filters(client: TestClient, session: Session, test_user: User, test_project: Project):
    """Entry filtreleme testi"""
    # Deney oluştur
    experiment = Experiment(
        project_id=test_project.id,
        title="Test Experiment",
        tags=["test"]
    )
    session.add(experiment)
    session.commit()
    session.refresh(experiment)
    
    # Birkaç entry oluştur
    for i in range(3):
        entry = Entry(
            experiment_id=experiment.id,
            author_id=test_user.id,
            title=f"Entry {i}",
            body_md=f"Content {i}",
            tags=["test", f"tag{i}"]
        )
        session.add(entry)
    session.commit()
    
    # Experiment ID ile filtrele
    response = client.get(f"/api/entries/?experiment_id={experiment.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    
    # Author ID ile filtrele
    response = client.get(f"/api/entries/?author_id={test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3


def test_project_not_found(client: TestClient):
    """Bulunamayan proje testi"""
    response = client.get("/api/projects/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_archive_project(client: TestClient, test_user: User, test_project: Project):
    """Proje arşivleme testi"""
    response = client.patch(
        f"/api/projects/{test_project.id}/archive?user_id={test_user.id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "archived"
    
    # Arşivlenmiş projeyi kontrol et
    response = client.get(f"/api/projects/{test_project.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["archived"] is True
