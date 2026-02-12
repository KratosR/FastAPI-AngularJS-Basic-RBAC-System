import { Instructor } from "./instructor.model";
import { Role } from "./role.model";
import { Student } from "./student.model";

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role_id: number;
  status: 'active' | 'inactive' | 'suspended';
  created_at: Date;
  role?: Role;
  student_detail?: Student | null;
  instructor_detail?: Instructor | null;
}
