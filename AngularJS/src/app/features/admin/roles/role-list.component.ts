import { Component, OnInit } from '@angular/core';
import { RoleService } from '../../../core/services/role.service';
import { Role, RoleCreate } from '../../../models/role.model';
import { Observable, map } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-role-list',
  templateUrl: './role-list.component.html',
  styleUrls: ['./role-list.component.scss']
})
export class RoleListComponent implements OnInit {
  roles$: Observable<Role[]>;
  roleMap = new Map<number, Role>();
  showCreateForm = false;
  newRole: RoleCreate = { role_name: '', parent_id: null };
  error = '';

  constructor(private roleService: RoleService) {
    this.roles$ = this.roleService.getRoles().pipe(
      map(roles => {
        roles.forEach(r => this.roleMap.set(r.id, r));
        return roles;
      })
    );
  }

  ngOnInit(): void {}

  getParentRoleName(parentId: number | null): string {
    if (!parentId) return '—';
    const parent = this.roleMap.get(parentId);
    return parent ? parent.role_name : `ID: ${parentId}`;
  }

  createRole(): void {
    if (!this.newRole.role_name.trim()) return;
    this.roleService.createRole(this.newRole).subscribe({
      next: (newRole) => {
        this.roles$ = this.roleService.getRoles().pipe(
          map(roles => {
            roles.forEach(r => this.roleMap.set(r.id, r));
            return roles;
          })
        );
        this.showCreateForm = false;
        this.newRole = { role_name: '', parent_id: null };
        this.error = '';
      },
      error: (err: HttpErrorResponse) => this.error = err.error?.detail || 'Creation failed'
    });
  }

  deleteRole(id: number): void {
    if (confirm('Are you sure? This action cannot be undone.')) {
      this.roleService.deleteRole(id).subscribe({
        next: () => {
          this.roles$ = this.roleService.getRoles().pipe(
            map(roles => {
              roles.forEach(r => this.roleMap.set(r.id, r));
              return roles;
            })
          );
        },
        error: (err: HttpErrorResponse) => alert(err.error?.detail || 'Delete failed')
      });
    }
  }
}
