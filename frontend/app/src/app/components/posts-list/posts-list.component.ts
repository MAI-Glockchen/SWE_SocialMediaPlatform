import { Component, OnInit } from '@angular/core';
import { PostsService, Post } from '../../../../services/posts.service';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-posts-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './posts-list.component.html',
})
export class PostsListComponent implements OnInit {
  posts: Post[] = [];

  constructor(private postsService: PostsService) {}

  ngOnInit() {
    this.postsService.getAll().subscribe(p => (this.posts = p));
  }

  img(p: Post) {
    return p.image ? `data:image/png;base64,${p.image}` : null;
  }
}
