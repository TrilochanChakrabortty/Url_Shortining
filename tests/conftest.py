import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app


# ============================================================
# TEST DATABASE
# ============================================================

TEST_DATABASE_URL = (
    "mysql+pymysql://root:trilochan@localhost:3306/"
    "url_shortener_test"
)


# ============================================================
# TEST DATABASE ENGINE
# ============================================================

test_engine = create_engine(TEST_DATABASE_URL)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# ============================================================
# CREATE TABLES
# ============================================================

@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    # Create all tables in the test database
    Base.metadata.create_all(bind=test_engine)

    yield

    # This will run after all tests are finished
    Base.metadata.drop_all(bind=test_engine)


# ============================================================
# DATABASE SESSION FIXTURE
# ============================================================

@pytest.fixture
def db():

    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )

    session = TestingSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ============================================================
# FASTAPI TEST CLIENT
# ============================================================

@pytest.fixture
def client(db):

    def override_get_db():

        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()