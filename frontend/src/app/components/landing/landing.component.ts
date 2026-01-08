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
  aiuser = '';
  manualuser = '';
  text = '';
  imageBase64: string | null = null;
  persona = 'neutral';
  prompt = '';  // AI Post prompt field

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
      user: this.manualuser?? this.aiuser,
      text: this.text,
      image: this.imageBase64,
    };

    this.postsService.create(payload).subscribe(() => {
      this.manualuser = '';
      this.aiuser = '';
      this.text = '';
      this.imageBase64 = null;
      this.loadPosts(); // refresh
    });
  }


  createAiPost() {

    const prompt = this.prompt || 'Create a short social media post';
    const payload = {
      user: this.aiuser || 'AI User',
      prompt: prompt,
      persona: this.persona || 'neutral',
      image: this.imageBase64,
    };

    this.postsService.createWithAI(payload).subscribe({
      next: () => {
        this.aiuser = '';
        this.text = '';
        this.imageBase64 = null;
        this.persona = 'neutral';
        this.loadPosts();
      },
      error: (err) => console.error('AI post failed', err),
    });
  }

  deletePost(id: number) {
    this.postsService.delete(id).subscribe(() => {
      this.loadPosts();
    });
  }

  img(post: Post): string {
    if (post.image_thumb) {
      return 'data:image/png;base64,' + post.image_thumb;
    }
    return 'default.png';
  }

}
