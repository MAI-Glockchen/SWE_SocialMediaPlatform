import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { ActivatedRoute } from '@angular/router';
import { PostDetailComponent } from './post-detail.component';
import { Post } from '../../../../services/posts.service';
import { Comment } from '../../../../services/comments.service';
import { describe, it, beforeEach, expect } from 'vitest';

describe('PostDetailComponent (Vitest)', () => {
  let fixture: ComponentFixture<PostDetailComponent>;
  let component: PostDetailComponent;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [PostDetailComponent],
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        {
          provide: ActivatedRoute,
          useValue: { snapshot: { paramMap: new Map([['id', '7']]) } }
        }
      ]
    });

    fixture = TestBed.createComponent(PostDetailComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('loads the post immediately', () => {
    const mockPost: Post = {
      id: 7,
      user: 'X',
      text: 'Hello',
      image: null,
      created_at: '2025-01-01T00:00:00Z'
    };

    fixture.detectChanges();

    httpMock.expectOne('http://localhost:8000/posts/7').flush(mockPost);

    expect(component.post()?.text).toBe('Hello');
  });

  it('loads comments (signal)', () => {
    const mockComments: Comment[] = [
      {
        comment_id: 1,
        super_id: 7,
        user: 'Joe',
        text: 'Nice',
        created_at: '2025-01-01T00:00:00Z'
      }
    ];

    fixture.detectChanges();

    httpMock.expectOne('http://localhost:8000/posts/7').flush({
      id: 7,
      user: 'X',
      text: 'Hello',
      image: null,
      created_at: '2025-01-01T00:00:00Z'
    });

    httpMock.expectOne('http://localhost:8000/posts/7/comments')
      .flush(mockComments);

    expect(component.comments().length).toBe(1);
    expect(component.comments()[0].text).toBe('Nice');
  });
});
