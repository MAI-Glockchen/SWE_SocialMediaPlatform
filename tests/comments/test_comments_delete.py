from tests.conftest import client, create_post, create_comment

def test_delete_comment():
    post_id = create_post()
    comment_id = create_comment(post_id)

    r = client.delete(f"/comments/{comment_id}")
    assert r.status_code == 204

    # confirm deletion
    assert client.get(f"/comments/{comment_id}").status_code == 404

def test_delete_nonexistent_comment():
    r = client.delete("/comments/999999")
    assert r.status_code == 404
