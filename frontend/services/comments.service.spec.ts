import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { CommentsService, Comment, CommentCreate } from './comments.service';
import { describe, it, expect, beforeEach } from 'vitest';

describe('CommentsService (Vitest)', () => {
  let service: CommentsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        CommentsService,
        provideHttpClient(),
        provideHttpClientTesting(),
      ]
    });
    service = TestBed.inject(CommentsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should fetch comments for a post', () => {
    const mock: Comment[] = [
      {
        comment_id: 1,
        super_id: 7,
        user: 'Bob',
        text: 'Nice!',
        created_at: '2025-01-01T00:00:00Z'
      }
    ];

    service.getForPost(7).subscribe(res => {
      expect(res.length).toBe(1);
      expect(res[0].text).toBe('Nice!');
    });

    const req = httpMock.expectOne('http://localhost:8000/posts/7/comments');
    expect(req.request.method).toBe('GET');
    req.flush(mock);
  });

  it('should create a comment using CommentCreate payload', () => {
    const payload: CommentCreate = { user: 'Bob', text: 'Cool' };

    const mock: Comment = {
      comment_id: 99,
      super_id: 7,
      user: 'Bob',
      text: 'Cool',
      created_at: '2025-01-01T00:00:00Z'
    };

    service.create(7, payload).subscribe(res => {
      expect(res.comment_id).toBe(99);
    });

    const req = httpMock.expectOne('http://localhost:8000/posts/7/comments');
    expect(req.request.method).toBe('POST');
    req.flush(mock);
  });
});
