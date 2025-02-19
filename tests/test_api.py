import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json == {'status': 'OK'}

def test_count(client):
    res = client.get("/count")
    assert res.status_code == 200
    assert res.json['length'] == 10

def test_data_contains_10_pictures(client):
    res = client.get("/picture")
    assert len(res.json) == 10

def test_get_picture(client):
    res = client.get("/picture")
    assert res.status_code == 200

def test_get_pictures_check_content_type_equals_json(client):
    res = client.get("/picture")
    assert res.headers["Content-Type"] == "application/json"

def test_get_picture_by_id(client):
    id_delete = 2
    res = client.get(f'/picture/{id_delete}')
    assert res.status_code == 200

def test_pictures_json_is_not_empty(client):
    res = client.get("/picture")
    assert len(res.json) > 0

@pytest.fixture
def picture():
    return {
        "id": 11,
        "event_city": "Fremont",
        "event_country": "United States",
        "event_date": "11/2/2030",
        "event_state": "California",
        "event_type": "Festival",
        "image": "image_url",
        "image_type": "jpg",
        "poster_email": "email@example.com",
        "poster_name": "John Doe",
        "poster_organization": "Example Org"
    }

def test_post_picture(picture, client):
    # create a brand new picture to upload
    res = client.post("/picture", data=json.dumps(picture),
                      content_type="application/json")
    assert res.status_code == 201

def test_post_picture_duplicate(picture, client):
    # create a brand new picture to upload
    res = client.post("/picture", data=json.dumps(picture),
                      content_type="application/json")
    assert res.status_code == 302
    assert res.json['message'] == f"Picture with id {picture['id']} already present"

def test_update_picture_by_id(client, picture):
    id = '2'
    res = client.get(f'/picture/{id}')
    res_picture = res.json
    assert res_picture['id'] == 2

def test_delete_picture_by_id(client):
    res = client.delete("/picture/11")
    assert res.status_code == 200
    assert res.json['message'] == "Picture deleted"

    res = client.get("/count")
    assert res.json['length'] == 10