import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

export interface Post {
  id: number;
  user: string;
  text: string;
  image: string | null;
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

  constructor(private http: HttpClient) {}

  getAll() {
    return this.http.get<Post[]>(`${this.api}/`);
  }

  getById(id: number) {
    return this.http.get<Post>(`${this.api}/${id}`);
  }

  create(payload: PostCreate) {
    return this.http.post<Post>(`${this.api}/`, payload);
  }
}
