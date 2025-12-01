import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PostsService } from '../../../../services/posts.service';
import { CommentsService } from '../../../../services/comments.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-post-detail',
  standalone: true,
  templateUrl: './post-detail.component.html',
  styleUrls: ['./post-detail.component.css'],
  imports: [CommonModule, FormsModule]
})
export class PostDetailComponent implements OnInit {
  post: any = null;
  comments: any[] = [];
  newText = '';
  newUser = '';

  constructor(
    private route: ActivatedRoute,
    private posts: PostsService,
    private commentsService: CommentsService
  ) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.posts.getById(id).subscribe(p => this.post = p);
    this.commentsService.getByPost(id).subscribe(c => this.comments = c);
  }

  img() {
    return this.post?.image ? `data:image/png;base64,${this.post.image}` : null;
  }

  addComment() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.commentsService.create(id, {
      text: this.newText,
      user: this.newUser
    }).subscribe(c => this.comments.push(c));
  }
}
