import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Comment {
  super_id: number;
  comment_id: number;
  text: string;
  user: string;
  created_at: string;
}

@Injectable({ providedIn: 'root' })
export class CommentsService {
  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getByPost(postId: number) {
    return this.http.get<Comment[]>(`${this.api}/posts/${postId}/comments`);
  }

  create(postId: number, data: { text: string; user: string }) {
    return this.http.post<Comment>(
      `${this.api}/posts/${postId}/comments`,
      data
    );
  }
}
