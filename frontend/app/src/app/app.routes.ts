import { Routes } from '@angular/router';
import { PostsListComponent } from './components/posts-list/posts-list.component';
import { PostDetailComponent } from './components/post-detail/post-detail.component';
import { PostCreateComponent } from './components/post-create/post-create.component';

export const routes: Routes = [
  { path: '', redirectTo: 'posts', pathMatch: 'full' },
  { path: 'posts', component: PostsListComponent },
  { path: 'create', component: PostCreateComponent },
  { path: 'post/:id', component: PostDetailComponent },
];
