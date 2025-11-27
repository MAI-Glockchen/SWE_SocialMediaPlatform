import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Post {
  id: number;
  image: string | null;
  text: string;
  user: string;
  created_at: string;
}

export interface PostCreate {
  image: string | null;
  text: string;
  user: string;
}

@Injectable({ providedIn: 'root' })
export class PostsService {
  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getAll() {
    return this.http.get<Post[]>(`${this.api}/posts/`);
  }

  getById(id: number) {
    return this.http.get<Post>(`${this.api}/posts/${id}`);
  }

  create(data: PostCreate) {
    return this.http.post<Post>(`${this.api}/posts/`, data);
  }
}
