import os
import pytest
from app import create_app
from db import init_db


@pytest.fixture()
def client(tmp_path):
    # Create a DB file path without pre-opening the file (avoids Windows lock issues)
    db_path = tmp_path / "test.sqlite3"

    os.environ["DATABASE_PATH"] = str(db_path)
    os.environ["SECRET_KEY"] = "test"

    app = create_app()
    app.config.update(TESTING=True)

    with app.app_context():
        init_db()

    with app.test_client() as c:
        yield c


def test_home_ok(client):
    r = client.get("/")
    assert r.status_code == 200


def test_add_task(client):
    r = client.post("/tasks", data={"title": "Task 1"}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Task 1" in r.data


def test_add_rejects_empty(client):
    r = client.post("/tasks", data={"title": "   "})
    assert r.status_code == 400
