import { describe, it, expect, vi } from 'vitest';
import { PostsService } from './posts.service';
import { HttpClient } from '@angular/common/http';

describe('PostsService (pure Vitest)', () => {
  it('should fetch all posts', () => {
    const getMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn([])
    });

    const http = { get: getMock } as unknown as HttpClient;
    const service = new PostsService(http);

    service.getAll().subscribe(() => { });

    expect(getMock).toHaveBeenCalledWith(
      'http://localhost:8000/posts/'
    );
  });

  it('should create a post', () => {
    const postMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn({})
    });

    const http = { post: postMock } as unknown as HttpClient;
    const service = new PostsService(http);

    service.create({
      user: 'u',
      text: 'hello',
      image: null
    }).subscribe(() => { });

    expect(postMock).toHaveBeenCalledWith(
      'http://localhost:8000/posts/',
      {
        user: 'u',
        text: 'hello',
        image: null
      }
    );
  });

  it('should delete a post', () => {
    const deleteMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn(null)
    });

    const http = { delete: deleteMock } as unknown as HttpClient;
    const service = new PostsService(http);

    service.delete(123).subscribe(() => { });

    expect(deleteMock).toHaveBeenCalledWith(
      'http://localhost:8000/posts/123'
    );
  });

});
