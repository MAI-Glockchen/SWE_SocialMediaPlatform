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

  newUser = '';
  newText = '';

  private route = inject(ActivatedRoute);
  private postsService = inject(PostsService);
  private commentsService = inject(CommentsService);

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadPost(id);
    this.loadComments(id);
  }

  loadPost(id: number) {
    this.postsService.getById(id).subscribe(p => this.post.set(p));
  }

  loadComments(id: number) {
    this.commentsService.getForPost(id).subscribe(c => this.comments.set(c));
  }

  submitComment() {
    const id = Number(this.route.snapshot.paramMap.get('id'));

    const payload: CommentCreate = {
      user: this.newUser,
      text: this.newText,
    };

    this.commentsService.create(id, payload).subscribe(() => {
      this.newUser = '';
      this.newText = '';
      this.loadComments(id);  // refresh list
    });
  }
}
