from tests.conftest import client, create_post

def test_search_comments_by_text():
    post_id = create_post()
    client.post(f"/posts/{post_id}/comments", json={"text": "FindMe123", "user": "bob"})
    client.post(f"/posts/{post_id}/comments", json={"text": "Other", "user": "charlie"})

    r = client.get(f"/posts/{post_id}/comments", params={"text": "FindMe123"})
    assert r.status_code == 200
    assert len(r.json()) == 1

def test_search_comments_by_user():
    post_id = create_post()
    client.post(f"/posts/{post_id}/comments", json={"text": "A", "user": "u1"})
    client.post(f"/posts/{post_id}/comments", json={"text": "B", "user": "u1"})
    client.post(f"/posts/{post_id}/comments", json={"text": "C", "user": "u2"})

    r = client.get(f"/posts/{post_id}/comments", params={"user": "u1"})
    assert len(r.json()) == 2

def test_search_comments_by_text_and_user():
    post_id = create_post()
    client.post(f"/posts/{post_id}/comments", json={"text": "UniqueABC", "user": "A"})
    client.post(f"/posts/{post_id}/comments", json={"text": "UniqueABC", "user": "B"})

    r = client.get(f"/posts/{post_id}/comments", params={"text": "UniqueABC", "user": "A"})
    assert len(r.json()) == 1
