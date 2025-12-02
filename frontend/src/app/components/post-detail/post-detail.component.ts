import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { PostsService, Post } from '../../../../services/posts.service';
import { CommentsService, CommentCreate, Comment } from '../../../../services/comments.service';

@Component({
  selector: 'app-post-detail',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './post-detail.component.html',
})
export class PostDetailComponent {

  post: Post | null = null;
  comments: Comment[] = [];

  newUser = '';
  newText = '';

  id = 0;

  constructor(
    private route: ActivatedRoute,
    private postsService: PostsService,
    private commentsService: CommentsService
  ) {}

  ngOnInit() {
    this.id = Number(this.route.snapshot.paramMap.get('id'));
    this.loadPost();
    this.loadComments();
  }

  loadPost() {
    this.postsService.getById(this.id).subscribe(p => this.post = p);
  }

  loadComments() {
    this.commentsService.getAllForPost(this.id)
      .subscribe(c => this.comments = c);
  }

  submitComment() {
    const payload: CommentCreate = {
      user: this.newUser,
      text: this.newText
    };

    this.commentsService.create(this.id, payload).subscribe(() => {
      this.newUser = '';
      this.newText = '';
      this.loadComments();
    });
  }

  img(post: Post | null) {
    if (post?.image) return `data:image/png;base64,${post.image}`;
    return '/assets/default.png';
  }
}
