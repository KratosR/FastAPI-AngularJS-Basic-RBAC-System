export interface Instructor {
  id: number;
  user_id: number;
  department: string;
  qualification: string;
  created_at: Date;
}

export interface InstructorCreate {
  user_id: number;
  department: string;
  qualification: string;
}

export interface InstructorUpdate {
  department?: string;
  qualification?: string;
}
