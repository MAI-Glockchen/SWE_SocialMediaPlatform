import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { LandingComponent } from './landing.component';
import { Post } from '../../../../services/posts.service';
import { describe, it, beforeEach, expect } from 'vitest';

describe('LandingComponent (Vitest)', () => {
  let fixture: ComponentFixture<LandingComponent>;
  let component: LandingComponent;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [LandingComponent],
      providers: [provideHttpClient(), provideHttpClientTesting()]
    });

    fixture = TestBed.createComponent(LandingComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should load posts via signals', () => {
    const mock: Post[] = [
      { id: 1, user: 'A', text: 'Hi', image: null, created_at: '2025-01-01T00:00:00Z' }
    ];

    fixture.detectChanges();

    httpMock.expectOne('http://localhost:8000/posts/').flush(mock);

    expect(component.posts().length).toBe(1);
  });

  it('should return default image when image is null', () => {
    const post: Post = {
      id: 1, user: 'A', text: 'Hi', image: null, created_at: '2025-01-01T00:00:00Z'
    };

    expect(component.img(post)).toBe('/default.png');
  });
});
