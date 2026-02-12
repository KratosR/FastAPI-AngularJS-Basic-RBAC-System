import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../core/services/auth.service';
import { UserService } from '../../../core/services/user.service';
import { User } from '../../../models/auth.model';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User | null = null;
  editMode = false;
  updateData = { email: '', status: '' };
  successMessage = '';

  constructor(
    public authService: AuthService,
    private userService: UserService
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.user = user;
      if (user) {
        this.updateData = { email: user.email, status: user.status };
      }
    });
  }

  toggleEdit(): void {
    this.editMode = !this.editMode;
  }

  updateProfile(): void {
    if (this.user) {
      this.userService.updateUser(this.user.id, {
        email: this.updateData.email,
        status: this.updateData.status as any
      }).subscribe({
        next: (updated) => {
          localStorage.setItem('current_user', JSON.stringify(updated));
          this.authService['currentUserSubject'].next(updated);
          this.user = updated;
          this.editMode = false;
          this.successMessage = 'Profile updated successfully.';
          setTimeout(() => this.successMessage = '', 3000);
        },
        error: (err) => console.error(err)
      });
    }
  }
}
