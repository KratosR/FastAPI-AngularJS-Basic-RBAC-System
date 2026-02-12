import { Component, OnInit } from '@angular/core';
import { InstructorService } from '../../../core/services/instructor.service';
import { UserService } from '../../../core/services/user.service';
import { Instructor, InstructorCreate, InstructorUpdate } from '../../../models/instructor.model';
import { User } from '../../../models/auth.model';
import { Observable, map } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-instructor-list',
  templateUrl: './instructor-list.component.html',
  styleUrls: ['./instructor-list.component.scss']
})
export class InstructorListComponent implements OnInit {
  instructors$: Observable<Instructor[]>;
  users$: Observable<User[]>;
  showCreateForm = false;
  newInstructor: InstructorCreate = {
    user_id: 0,
    department: '',
    qualification: ''
  };
  error = '';
  editing = false;
  editingId: number | null = null;

  constructor(
    private instructorService: InstructorService,
    private userService: UserService
  ) {
    this.instructors$ = this.instructorService.getInstructors();
    this.users$ = this.userService.getUsers().pipe(
      map(users => users.filter(u => u.role?.role_name === 'instructor' && !u.instructor_detail))
    );
  }

  ngOnInit(): void {}

  createInstructor(): void {
    if (!this.newInstructor.user_id || !this.newInstructor.department.trim() || !this.newInstructor.qualification.trim()) {
      this.error = 'All fields are required.';
      return;
    }
    this.instructorService.createInstructor(this.newInstructor).subscribe({
      next: () => {
        this.instructors$ = this.instructorService.getInstructors();
        this.showCreateForm = false;
        this.newInstructor = { user_id: 0, department: '', qualification: '' };
        this.error = '';
        this.users$ = this.userService.getUsers().pipe(
          map(users => users.filter(u => u.role?.role_name === 'instructor' && !u.instructor_detail))
        );
      },
      error: (err: HttpErrorResponse) => this.error = err.error?.detail || 'Creation failed'
    });
  }

  deleteInstructor(id: number): void {
    if (confirm('Are you sure?')) {
      this.instructorService.deleteInstructor(id).subscribe({
        next: () => {
          this.instructors$ = this.instructorService.getInstructors();
          this.users$ = this.userService.getUsers().pipe(
            map(users => users.filter(u => u.role?.role_name === 'instructor' && !u.instructor_detail))
          );
        },
        error: (err: HttpErrorResponse) => alert(err.error?.detail || 'Delete failed')
      });
    }
  }

  updateInstructor(instructor: Instructor): void {
    const update: InstructorUpdate = {
      department: instructor.department,
      qualification: instructor.qualification
    };
    this.instructorService.updateInstructor(instructor.id, update).subscribe({
      next: () => {
        this.instructors$ = this.instructorService.getInstructors();
        this.editing = false;
        this.editingId = null;
      },
      error: (err: HttpErrorResponse) => alert(err.error?.detail || 'Update failed')
    });
  }

  startEdit(instructor: Instructor): void {
    this.editing = true;
    this.editingId = instructor.id;
  }

  saveEdit(instructor: Instructor): void {
    this.updateInstructor(instructor);
  }

  cancelEdit(): void {
    this.editing = false;
    this.editingId = null;
    this.instructors$ = this.instructorService.getInstructors(); // refresh to discard changes
  }
}
