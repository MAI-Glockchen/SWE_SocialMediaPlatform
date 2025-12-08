from tests.conftest import client, create_post

def test_get_all_posts():
    create_post()
    create_post()
    create_post()

    r = client.get("/posts/")
    assert r.status_code == 200

    posts = r.json()
    assert len(posts) >= 3

def test_get_post_by_id():
    post_id = create_post(text="test-text")

    r = client.get(f"/posts/{post_id}")
    assert r.status_code == 200

    data = r.json()
    assert data["id"] == post_id
    assert data["text"] == "test-text"

def test_get_post_not_found():
    r = client.get("/posts/99999999")
    assert r.status_code == 404
