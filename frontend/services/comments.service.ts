import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Comment {
  super_id: number;
  comment_id: number;
  user: string;
  text: string;
  created_at: string;
}

export interface CommentCreate {
  user: string;
  text: string;
}

@Injectable({ providedIn: 'root' })
export class CommentsService {

  private api = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  getAllForPost(postId: number): Observable<Comment[]> {
    return this.http.get<Comment[]>(`${this.api}/posts/${postId}/comments`);
  }

  create(postId: number, payload: CommentCreate): Observable<Comment> {
    return this.http.post<Comment>(`${this.api}/posts/${postId}/comments`, payload);
  }
}
