import { Routes } from '@angular/router';
import { LandingComponent } from './components/landing/landing.component';
import { PostDetailComponent } from './components/post-detail/post-detail.component';

export const routes: Routes = [
  { path: '', component: LandingComponent },
  { path: 'post/:id', component: PostDetailComponent }
];
