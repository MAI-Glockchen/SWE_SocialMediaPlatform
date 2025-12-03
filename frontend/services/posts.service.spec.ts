import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { PostsService, Post, PostCreate } from './posts.service';
import { describe, it, expect, beforeEach } from 'vitest';

describe('PostsService (Vitest)', () => {
  let service: PostsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        PostsService,
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    });
    service = TestBed.inject(PostsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should fetch all posts', () => {
    const mockPosts: Post[] = [
      { id: 1, user: 'A', text: 'Hello', image: null, created_at: '2025-01-01T00:00:00Z' }
    ];

    service.getAll().subscribe(res => {
      expect(res.length).toBe(1);
      expect(res[0].user).toBe('A');
    });

    const req = httpMock.expectOne('http://localhost:8000/posts/');
    expect(req.request.method).toBe('GET');
    req.flush(mockPosts);
  });

  it('should create a post using PostCreate payload', () => {
    const payload: PostCreate = { user: 'A', text: 'Hello', image: null };

    const mockResponse: Post = {
      id: 99,
      user: 'A',
      text: 'Hello',
      image: null,
      created_at: '2025-01-01T00:00:00Z'
    };

    service.create(payload).subscribe(res => {
      expect(res.id).toBe(99);
      expect(res.user).toBe('A');
    });

    const req = httpMock.expectOne('http://localhost:8000/posts/');
    expect(req.request.method).toBe('POST');
    req.flush(mockResponse);
  });
});
