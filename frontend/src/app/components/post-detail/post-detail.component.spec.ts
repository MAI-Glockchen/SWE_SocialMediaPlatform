import { describe, it, expect, vi } from 'vitest';
import type { Post } from '../../../../services/posts.service';
import type { Comment } from '../../../../services/comments.service';

// Pure fake without Angular DI:
class FakePostDetailComponent {
  post = vi.fn(() => this._post);
  comments = vi.fn(() => this._comments);

  _post: Post | null = null;
  _comments: Comment[] = [];

  postsService: any;
  commentsService: any;

  loadPost(id: number) {
    this.postsService.getById(id).subscribe((p: Post) => (this._post = p));
  }

  loadComments(id: number) {
    this.commentsService.getForPost(id).subscribe((c: Comment[]) => (this._comments = c));
  }
}

describe('PostDetailComponent (pure Vitest)', () => {
  it('should load the post immediately', () => {
    const mockPost: Post = {
      id: 1,
      text: 'hello',
      user: 'u',
      image: null,
      created_at: '2024-01-01T00:00:00Z',
    };

    const getByIdMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn(mockPost),
    });

    const comp = new FakePostDetailComponent();
    comp.postsService = { getById: getByIdMock };
    comp.commentsService = { getForPost: () => ({ subscribe() {} }) };

    comp.loadPost(1);

    expect(getByIdMock).toHaveBeenCalledWith(1);
    expect(comp._post).toEqual(mockPost);
  });

  it('should load comments (signal)', () => {
    const mockComments: Comment[] = [
      {
        super_id: 1,
        comment_id: 1,
        user: 'u',
        text: 'hi',
        created_at: '2024-01-02T00:00:00Z',
      },
    ];

    const getForPostMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn(mockComments),
    });

    const comp = new FakePostDetailComponent();
    comp.postsService = { getById: () => ({ subscribe() {} }) };
    comp.commentsService = { getForPost: getForPostMock };

    comp.loadComments(1);

    expect(getForPostMock).toHaveBeenCalledWith(1);
    expect(comp._comments).toEqual(mockComments);
  });
});
