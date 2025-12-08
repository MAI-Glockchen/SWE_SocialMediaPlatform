import { describe, it, expect, vi } from 'vitest';
import { CommentsService } from './comments.service';
import { HttpClient } from '@angular/common/http';

describe('CommentsService (pure Vitest)', () => {
  it('should fetch comments for a post', () => {
    const getMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn([])
    });

    const http = { get: getMock } as unknown as HttpClient;
    const service = new CommentsService(http);

    service.getForPost(1).subscribe(() => { });

    expect(getMock).toHaveBeenCalledWith(
      'http://localhost:8000/posts/1/comments'
    );
  });

  it('should create a comment', () => {
    const postMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn({})
    });

    const http = { post: postMock } as unknown as HttpClient;
    const service = new CommentsService(http);

    service.create(1, {
      user: 'a',
      text: 'b'
    }).subscribe(() => { });

    expect(postMock).toHaveBeenCalledWith(
      'http://localhost:8000/posts/1/comments',
      {
        user: 'a',
        text: 'b'
      }
    );
  });
  
  it('should delete a comment', () => {
    const deleteMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn(null)
    });

    const http = { delete: deleteMock } as unknown as HttpClient;
    const service = new CommentsService(http);

    service.delete(55).subscribe(() => { });

    expect(deleteMock).toHaveBeenCalledWith(
      'http://localhost:8000/comments/55'
    );
  });


});
