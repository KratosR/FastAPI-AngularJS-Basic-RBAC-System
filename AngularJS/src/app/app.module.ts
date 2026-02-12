import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { JwtInterceptor } from './core/interceptors/jwt.interceptor';

// Shared
import { NavbarComponent } from './shared/components/navbar/navbar.component';
import { FooterComponent } from './shared/components/footer/footer.component';
import { ForbiddenComponent } from './shared/components/forbidden/forbidden.component';
import { NotFoundComponent } from './shared/components/not-found/not-found.component';

// Features
import { LoginComponent } from './features/auth/login/login.component';
import { ProfileComponent } from './features/auth/profile/profile.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';

// Admin
import { RoleListComponent } from './features/admin/roles/role-list.component';
import { UserListComponent } from './features/admin/users/user-list.component';
import { InstructorListComponent } from './features/admin/instructors/instructor-list.component';

// Instructor
import { StudentListComponent } from './features/instructor/students/student-list.component';
import { StudentFormComponent } from './features/instructor/students/student-form.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    ForbiddenComponent,
    NotFoundComponent,
    LoginComponent,
    ProfileComponent,
    DashboardComponent,
    RoleListComponent,
    UserListComponent,
    InstructorListComponent,
    StudentListComponent,
    StudentFormComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,           // <-- required for ngModel, ngForm
    ReactiveFormsModule,   // <-- for reactive forms (optional but good)
    CommonModule           // <-- required for *ngIf, *ngFor, async, date
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
