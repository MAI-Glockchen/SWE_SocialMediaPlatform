from tests.conftest import client, create_post

def test_search_posts_by_text():
    create_post(text="Search test 123")

    r = client.get("/posts/", params={"text": "Search test 123"})
    assert r.status_code == 200

    data = r.json()
    assert len(data) >= 1
    assert "Search" in data[0]["text"]

def test_search_posts_by_user():
    create_post(text="Hello", user="testerA")
    create_post(text="World", user="testerA")

    r = client.get("/posts/", params={"user": "testerA"})
    assert r.status_code == 200

    assert all(post["user"] == "testerA" for post in r.json())

def test_search_posts_by_text_and_user():
    create_post(text="UniqueXYZ", user="unique_user")

    r = client.get("/posts/", params={"text": "UniqueXYZ", "user": "unique_user"})
    assert r.status_code == 200

    data = r.json()
    assert len(data) == 1
    assert data[0]["user"] == "unique_user"

def test_search_no_results():
    r = client.get("/posts/", params={"text": "doesnotexist", "user": "nouser"})
    assert r.status_code == 404
