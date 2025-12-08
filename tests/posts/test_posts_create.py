from tests.conftest import client, encode_image

def test_create_post():
    payload = {
        "image": encode_image("hello.png"),
        "text": "Hello world",
        "user": "alice",
    }

    r = client.post("/posts/", json=payload)
    assert r.status_code == 200

    data = r.json()
    assert data["user"] == "alice"
    assert "created_at" in data
