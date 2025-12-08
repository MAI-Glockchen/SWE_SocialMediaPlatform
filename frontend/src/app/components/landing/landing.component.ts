import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { PostsService, PostCreate, Post } from '../../../../services/posts.service';
import { NgIconsModule } from '@ng-icons/core';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [FormsModule, NgIconsModule, RouterLink],
  templateUrl: './landing.component.html',
})
export class LandingComponent {

  posts = signal<Post[]>([]);

  // new post form fields
  user = '';
  text = '';
  imageBase64: string | null = null;

  constructor(private postsService: PostsService) { }

  ngOnInit() {
    this.loadPosts();
  }

  loadPosts() {
    this.postsService.getAll().subscribe(p => this.posts.set(p));

  }

  onImage(event: any) {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => this.imageBase64 = reader.result as string;
    reader.readAsDataURL(file);
  }

  submitPost() {
    const payload: PostCreate = {
      user: this.user,
      text: this.text,
      image: this.imageBase64,
    };

    this.postsService.create(payload).subscribe(() => {
      this.user = '';
      this.text = '';
      this.imageBase64 = null;
      this.loadPosts(); // refresh
    });
  }

  deletePost(id: number) {
    this.postsService.delete(id).subscribe(() => {
      this.loadPosts();
    });
  }

  img(post: Post) {
    if (post.image) return `data:image/png;base64,${post.image}`;
    return 'default.png'; // default placeholder image
  }
}
