import { Component, signal, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { PostsService } from '../../../../services/posts.service';
import { CommentsService } from '../../../../services/comments.service';
import { Post } from '../../../../services/posts.service';
import { CommentCreate, Comment } from '../../../../services/comments.service';

@Component({
  selector: 'app-post-detail',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './post-detail.component.html',
})
export class PostDetailComponent {

  post = signal<Post | null>(null);
  comments = signal<Comment[]>([]);

  postId!: number;
  newUser = '';
  newText = '';

  private route = inject(ActivatedRoute);
  private postsService = inject(PostsService);
  private commentsService = inject(CommentsService);

  ngOnInit() {
    this.postId = Number(this.route.snapshot.paramMap.get('id'));

    this.loadPost(this.postId);
    this.loadComments(this.postId);
  }

  loadPost(postId: number) {
    this.postsService.getById(postId).subscribe(p => this.post.set(p));
  }

  loadComments(postId: number) {
    this.commentsService.getForPost(postId).subscribe(c => this.comments.set(c));
  }

  submitComment() {
    const payload: CommentCreate = {
      user: this.newUser,
      text: this.newText,
    };

    this.commentsService.create(this.postId, payload).subscribe(() => {
      this.newUser = '';
      this.newText = '';
      this.loadComments(this.postId);  // refresh
    });
  }

  deleteComment(commentId: number) {
    this.commentsService.delete(commentId).subscribe(() => {
      this.loadComments(this.postId);
    });
  }

}
