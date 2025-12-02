import { Component } from '@angular/core';
import { PostsService } from '../../../../services/posts.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-post-create',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './post-create.component.html',
})
export class PostCreateComponent {

  user = '';
  text = '';
  imageBase64: string | null = null;

  constructor(
    private postsService: PostsService,
    private router: Router
  ) {}

  submit() {
    this.postsService.create({
      user: this.user,
      text: this.text,
      image: this.imageBase64,
    }).subscribe(() => {
      this.router.navigate(['/posts']); // Redirect after success
    });
  }

  onImage(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      this.imageBase64 = reader.result as string;
    };
    reader.readAsDataURL(file);
  }
}
