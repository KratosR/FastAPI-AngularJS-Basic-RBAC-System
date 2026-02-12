import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth.guard';

import { LoginComponent } from './features/auth/login/login.component';
import { ProfileComponent } from './features/auth/profile/profile.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { RoleListComponent } from './features/admin/roles/role-list.component';
import { UserListComponent } from './features/admin/users/user-list.component';
import { InstructorListComponent } from './features/admin/instructors/instructor-list.component';
import { StudentListComponent } from './features/instructor/students/student-list.component';
import { StudentFormComponent } from './features/instructor/students/student-form.component';
import { ForbiddenComponent } from './shared/components/forbidden/forbidden.component';
import { NotFoundComponent } from './shared/components/not-found/not-found.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },

  // Admin routes
  {
    path: 'admin',
    canActivate: [AuthGuard],
    data: { role: 'admin' },
    children: [
      { path: 'roles', component: RoleListComponent },
      { path: 'users', component: UserListComponent },
      { path: 'instructors', component: InstructorListComponent }
    ]
  },

  // Instructor routes
  {
    path: 'instructor',
    canActivate: [AuthGuard],
    data: { role: 'instructor' },
    children: [
      { path: 'students', component: StudentListComponent },
      { path: 'students/new', component: StudentFormComponent },
      { path: 'students/edit/:id', component: StudentFormComponent }
    ]
  },

  { path: 'forbidden', component: ForbiddenComponent },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
