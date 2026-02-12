import { Component, OnInit } from '@angular/core';
import { StudentService } from '../../../core/services/student.service';
import { Student } from '../../../models/student.model';
import { Observable } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-student-list',
  templateUrl: './student-list.component.html',
  styleUrls: ['./student-list.component.scss']
})
export class StudentListComponent implements OnInit {
  students$: Observable<Student[]>;
  selectedStudent: Student | null = null;
  isEditing = false;
  editingId: number | null = null;

  constructor(private studentService: StudentService) {
    this.students$ = this.studentService.getStudents();
  }

  ngOnInit(): void {}

  deleteStudent(id: number): void {
    if (confirm('Are you sure? This action is irreversible.')) {
      this.studentService.deleteStudent(id).subscribe({
        next: () => {
          this.students$ = this.studentService.getStudents();
        },
        error: (err: HttpErrorResponse) => {
          if (err.status === 403) {
            alert('You do not have permission to delete students.');
          }
        }
      });
    }
  }

  editStudent(student: Student): void {
    this.selectedStudent = { ...student };
    this.isEditing = true;
    this.editingId = student.id;
  }

  cancelEdit(): void {
    this.selectedStudent = null;
    this.isEditing = false;
    this.editingId = null;
  }

  updateStudent(): void {
    if (this.selectedStudent) {
      const { id, ...updateData } = this.selectedStudent;
      this.studentService.updateStudent(id, updateData).subscribe({
        next: () => {
          this.cancelEdit();
          this.students$ = this.studentService.getStudents();
        },
        error: (err: HttpErrorResponse) => {
          alert(err.error?.detail || 'Update failed');
        }
      });
    }
  }
}
