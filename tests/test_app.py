import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import app


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_cafe_page():
    client = app.test_client()

    response = client.get("/cafe/1")

    assert response.status_code == 200


def test_invalid_cafe():
    client = app.test_client()

    response = client.get("/cafe/999")

    assert response.status_code == 404


def test_search_by_location():
    client = app.test_client()

    response = client.get("/?search=Mumbai")

    assert response.status_code == 200
    assert b"Brew &amp; Bloom" in response.data


def test_search_no_results():
    client = app.test_client()

    response = client.get("/?search=xyz123")

    assert response.status_code == 200
    assert b"No cafes found" in response.data