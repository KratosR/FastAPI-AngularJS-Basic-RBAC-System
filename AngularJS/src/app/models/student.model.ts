export interface Student {
  id: number;
  user_id: number;
  enrollment_no: string;
  course: string;
  year: number;
  created_at: Date;
}

export interface StudentCreate {
  user_id: number;
  enrollment_no: string;
  course: string;
  year: number;
}

export interface StudentUpdate {
  enrollment_no?: string;
  course?: string;
  year?: number;
}
