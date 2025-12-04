from tests.conftest import client, create_post, create_comment

def test_get_comments_for_post():
    post_id = create_post()
    create_comment(post_id, user="bob")
    create_comment(post_id, user="carol")

    r = client.get(f"/posts/{post_id}/comments")
    assert r.status_code == 200
    assert len(r.json()) >= 2

def test_get_comment_by_id():
    post_id = create_post()
    comment_id = create_comment(post_id, text="unique", user="dave")

    r = client.get(f"/comments/{comment_id}")
    assert r.status_code == 200
    assert r.json()["text"] == "unique"
