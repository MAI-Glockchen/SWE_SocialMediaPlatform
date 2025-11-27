import { Component, OnInit } from '@angular/core';
import { PostsService, Post } from '../../../../services/posts.service'
import { RouterLink } from '@angular/router';
import { NgFor, NgIf } from '@angular/common';

@Component({
  selector: 'app-posts-list',
  standalone: true,
  imports: [NgFor, NgIf, RouterLink],
  templateUrl: './posts-list.component.html',
})
export class PostsListComponent implements OnInit {
  posts: Post[] = [];

  constructor(private postsService: PostsService) {}

  ngOnInit() {
    this.postsService.getAll().subscribe(p => this.posts = p);
  }

  img(p: Post) {
    return p.image ? `data:image/png;base64,${p.image}` : null;
  }
}
