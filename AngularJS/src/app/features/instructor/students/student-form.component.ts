import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { StudentService } from '../../../core/services/student.service';
import { UserService } from '../../../core/services/user.service';
import { Student, StudentCreate, StudentUpdate } from '../../../models/student.model';
import { User } from '../../../models/auth.model';
import { Observable, map } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-student-form',
  templateUrl: './student-form.component.html',
  styleUrls: ['./student-form.component.scss']
})
export class StudentFormComponent implements OnInit {
  isEdit = false;
  studentId: number | null = null;
  student: StudentCreate | StudentUpdate = {
    user_id: 0,
    enrollment_no: '',
    course: '',
    year: 1
  };
  users$: Observable<User[]>;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private studentService: StudentService,
    private userService: UserService
  ) {
    this.users$ = this.userService.getUsers().pipe(
      map(users => users.filter(u => u.role?.role_name === 'student' && !u.student_detail))
    );
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.studentId = +id;
      this.studentService.getStudent(this.studentId).subscribe({
        next: (data: Student) => {
          this.student = {
            user_id: data.user_id,
            enrollment_no: data.enrollment_no,
            course: data.course,
            year: data.year
          };
        },
        error: (err: HttpErrorResponse) => {
          this.error = 'Student not found.';
        }
      });
    }
  }

  onSubmit(): void {
    if (this.isEdit && this.studentId) {
      this.studentService.updateStudent(this.studentId, this.student as StudentUpdate).subscribe({
        next: () => this.router.navigate(['/instructor/students']),
        error: (err: HttpErrorResponse) => {
          this.error = err.error?.detail || 'Update failed';
        }
      });
    } else {
      this.studentService.createStudent(this.student as StudentCreate).subscribe({
        next: () => this.router.navigate(['/instructor/students']),
        error: (err: HttpErrorResponse) => {
          this.error = err.error?.detail || 'Creation failed';
        }
      });
    }
  }
}
