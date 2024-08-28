import os
import tempfile

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db
from app.models import File
from app.services.filesystem_service import FileSystemService


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def temp_file() -> tempfile.NamedTemporaryFile:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    yield temp_file
    os.remove(temp_file.name)


def test_upload_file(client: FlaskClient, temp_file: tempfile.NamedTemporaryFile):
    temp_file.write(b"test content")
    temp_file.seek(0)

    data = {"file": (temp_file, "testfile.txt")}
    response = client.post(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        auth=("user1", "password1"),
    )
    assert response.status_code == 201
    assert "file_hash" in response.json


def test_download_file(
    client: FlaskClient, app: Flask, temp_file: tempfile.NamedTemporaryFile
):
    file_hash = "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2"
    file_record = File(file_hash=file_hash, filename="testfile.txt", username="user1")

    with app.app_context():
        file_path = FileSystemService.get_file_path(file_hash)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        db.session.add(file_record)
        db.session.commit()

        with open(file_path, "wb") as f:
            f.write(b"test content")

        response = client.get(f"/download/{file_hash}")
        assert response.status_code == 200
        assert response.data == b"test content"


def test_delete_file(
    client: FlaskClient, app: Flask, temp_file: tempfile.NamedTemporaryFile
):
    file_hash = "d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2"
    file_record = File(file_hash=file_hash, filename="testfile.txt", username="user1")

    with app.app_context():
        file_path = FileSystemService.get_file_path(file_hash)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        db.session.add(file_record)
        db.session.commit()

        with open(file_path, "wb") as f:
            f.write(b"test content")

        response = client.delete(f"/delete/{file_hash}", auth=("user1", "password1"))
        assert response.status_code == 200
        assert "File deleted." in response.json["message"]
        assert not os.path.isfile(file_path)
