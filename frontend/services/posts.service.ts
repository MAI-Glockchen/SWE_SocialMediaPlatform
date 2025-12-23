import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

export interface Post {
  id: number;
  user: string;
  text: string;
  image_full: string | null;
  image_thumb: string | null;
  created_at: string; // backend returns a string timestamp
}

export interface PostCreate {
  user: string;
  text: string;
  image: string | null;
}

@Injectable({ providedIn: 'root' })
export class PostsService {
  private api = 'http://localhost:8000/posts';

  constructor(private http: HttpClient) { }

  getAll() {
    return this.http.get<Post[]>(`${this.api}/`);
  }

  getById(id: number) {
    return this.http.get<Post>(`${this.api}/${id}`);
  }

  create(payload: PostCreate) {
    return this.http.post<Post>(`${this.api}/`, payload);
  }

  // Neuer Endpunkt: Erzeuge einen Post mit AI (Backend: POST /posts/generate)
  createWithAI(payload: { user: string; prompt: string; persona?: string; image?: string | null }) {
    // default to background queueing
    return this.http.post<Post>(`${this.api}/generate`, payload);
  }



  delete(id: number) {
    return this.http.delete<void>(`${this.api}/${id}`);
  }

}
