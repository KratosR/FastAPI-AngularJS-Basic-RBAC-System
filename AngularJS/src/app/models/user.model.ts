export interface UserCreate {
  username: string;
  email: string;
  password: string;
  role_id: number;
  status: 'active' | 'inactive' | 'suspended';
}

export interface UserUpdate {
  email?: string;
  status?: 'active' | 'inactive' | 'suspended';
  role_id?: number;
}
