import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Instructor, InstructorCreate, InstructorUpdate } from '../../models/instructor.model';

@Injectable({
  providedIn: 'root'
})
export class InstructorService {
  private apiUrl = `${environment.apiUrl}/instructors`;

  constructor(private http: HttpClient) {}

  getInstructors(): Observable<Instructor[]> {
    return this.http.get<Instructor[]>(this.apiUrl);
  }

  getInstructor(id: number): Observable<Instructor> {
    return this.http.get<Instructor>(`${this.apiUrl}/${id}`);
  }

  getInstructorByUser(userId: number): Observable<Instructor> {
    return this.http.get<Instructor>(`${this.apiUrl}/by-user/${userId}`);
  }

  createInstructor(instructor: InstructorCreate): Observable<Instructor> {
    return this.http.post<Instructor>(this.apiUrl, instructor);
  }

  updateInstructor(id: number, instructor: InstructorUpdate): Observable<Instructor> {
    return this.http.patch<Instructor>(`${this.apiUrl}/${id}`, instructor);
  }

  deleteInstructor(id: number): Observable<Instructor> {
    return this.http.delete<Instructor>(`${this.apiUrl}/${id}`);
  }
}
