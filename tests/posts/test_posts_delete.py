from tests.conftest import client, create_comment, create_post


def test_delete_post_and_its_comments():
    post_id = create_post()

    c1 = create_comment(post_id)
    c2 = create_comment(post_id)

    r = client.delete(f"/posts/{post_id}")
    assert r.status_code == 204

    # Post gone
    assert client.get(f"/posts/{post_id}").status_code == 404
    # Comments gone
    assert client.get(f"/comments/{c1}").status_code == 404
    assert client.get(f"/comments/{c2}").status_code == 404


def test_delete_nonexistent_post():
    r = client.delete("/posts/999999")
    assert r.status_code == 404
