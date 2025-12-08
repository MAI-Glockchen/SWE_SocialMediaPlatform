import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

export interface Comment {
  comment_id: number;
  super_id: number;
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
  private api = 'http://localhost:8000/posts';

  constructor(private http: HttpClient) { }

  getForPost(postId: number) {
    return this.http.get<Comment[]>(`${this.api}/${postId}/comments`);
  }

  create(postId: number, payload: CommentCreate) {
    return this.http.post<Comment>(`${this.api}/${postId}/comments`, payload);
  }
  
  delete(commentId: number) {
    return this.http.delete<void>(`${this.api}/comments/${commentId}`);
  }

}
