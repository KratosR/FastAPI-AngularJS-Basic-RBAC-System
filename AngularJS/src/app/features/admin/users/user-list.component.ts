import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../core/services/user.service';
import { RoleService } from '../../../core/services/role.service';
import { User } from '../../../models/auth.model';
import { UserCreate, UserUpdate } from '../../../models/user.model';
import { Role } from '../../../models/role.model';
import { Observable, combineLatest, map } from 'rxjs';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss']
})
export class UserListComponent implements OnInit {
  users$: Observable<User[]>;
  roles$: Observable<Role[]>;
  showCreateForm = false;
  newUser: UserCreate = {
    username: '',
    email: '',
    password: '',
    role_id: 0,
    status: 'active'
  };
  error = '';

  constructor(
    private userService: UserService,
    private roleService: RoleService
  ) {
    this.users$ = this.userService.getUsers();
    this.roles$ = this.roleService.getRoles();
  }

  ngOnInit(): void {}

  createUser(): void {
    if (!this.newUser.username.trim() || !this.newUser.email.trim() || !this.newUser.password.trim() || !this.newUser.role_id) {
      this.error = 'All fields are required.';
      return;
    }
    this.userService.createUser(this.newUser).subscribe({
      next: () => {
        this.users$ = this.userService.getUsers();
        this.showCreateForm = false;
        this.newUser = { username: '', email: '', password: '', role_id: 0, status: 'active' };
        this.error = '';
      },
      error: (err) => this.error = err.error.detail || 'Creation failed'
    });
  }

  deleteUser(id: number): void {
    if (confirm('Are you sure? This will also delete any associated student/instructor record.')) {
      this.userService.deleteUser(id).subscribe({
        next: () => this.users$ = this.userService.getUsers(),
        error: (err) => alert(err.error.detail || 'Delete failed')
      });
    }
  }

  updateStatus(user: User, status: 'active' | 'inactive' | 'suspended'): void {
    this.userService.updateUser(user.id, { status }).subscribe({
      next: (updated) => {
        this.users$ = this.userService.getUsers();
      },
      error: (err) => alert(err.error.detail || 'Update failed')
    });
  }
}
