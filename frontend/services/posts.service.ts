import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Post {
  id: number;
  user: string;
  text: string;
  image: string | null; // base64
  created_at: string;
}

export interface PostCreate {
  user: string;
  text: string;
  image: string | null;
}

@Injectable({ providedIn: 'root' })
export class PostsService {

  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Post[]> {
    return this.http.get<Post[]>(`${this.api}/posts/`);
  }

  getById(id: number): Observable<Post> {
    return this.http.get<Post>(`${this.api}/posts/${id}`);
  }

  create(payload: PostCreate): Observable<Post> {
    return this.http.post<Post>(`${this.api}/posts/`, payload);
  }
}
