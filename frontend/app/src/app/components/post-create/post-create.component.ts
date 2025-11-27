import { Component } from '@angular/core';
import { PostsService } from '../../../../services/posts.service';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-post-create',
  standalone: true,
  imports: [NgIf],
  templateUrl: './post-create.component.html',
})
export class PostCreateComponent {
  text = '';
  user = '';
  imageBase64: string | null = null;

  constructor(private posts: PostsService) {}

  onImage(e: any) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = () => this.imageBase64 = reader.result as string;
    reader.readAsDataURL(file);
  }

  submit() {
    this.posts.create({
      image: this.imageBase64,
      text: this.text,
      user: this.user,
    }).subscribe();
  }
}
