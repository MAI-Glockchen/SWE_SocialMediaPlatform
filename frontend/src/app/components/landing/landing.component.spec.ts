import { describe, it, expect, vi } from 'vitest';
import { LandingComponent } from './landing.component';
import { PostsService } from '../../../../services/posts.service';
import type { Post } from '../../../../services/posts.service';

describe('LandingComponent (pure Vitest)', () => {
  it('should load posts via signals', () => {
    const mockPosts: Post[] = [
      {
        id: 1,
        text: 'hello',
        image_thumb: null,
        image_full: null,
        user: 'u',
        created_at: '2024-01-01T00:00:00Z'
      }
    ];

    const getAllMock = vi.fn().mockReturnValue({
      subscribe: (fn: any) => fn(mockPosts)
    });

    const postsService = { getAll: getAllMock } as unknown as PostsService;

    const comp = new LandingComponent(postsService);
    comp.ngOnInit();

    expect(comp.posts()).toEqual(mockPosts);
  });

  it('img() should return default placeholder when image_thumb is null', () => {
    const postsService = { getAll: () => ({ subscribe: () => { } }) } as any;

    const comp = new LandingComponent(postsService);

    const post: Post = {
      id: 1,
      text: 'x',
      user: 'u',
      image_thumb: null,
      image_full: null,
      created_at: '2024-01-01T00:00:00Z'
    };

    expect(comp.img(post)).toBe('default.png');
  });

  it('img() should return base64 data-url when image_thumb exists', () => {
    const postsService = { getAll: () => ({ subscribe: () => { } }) } as any;

    const comp = new LandingComponent(postsService);

    const post: Post = {
      id: 1,
      text: 'x',
      user: 'u',
      image_thumb: 'AAAA',
      image_full: null,
      created_at: '2024-01-01T00:00:00Z'
    };

    expect(comp.img(post)).toBe('data:image/png;base64,AAAA');
  });
});
