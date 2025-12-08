from tests.conftest import client, create_post

def test_create_comment():
    post_id = create_post()

    payload = {"text": "nice post", "user": "alice"}
    r = client.post(f"/posts/{post_id}/comments", json=payload)

    assert r.status_code == 200
    data = r.json()

    assert data["text"] == "nice post"
    assert data["user"] == "alice"
    assert data["super_id"] == post_id
