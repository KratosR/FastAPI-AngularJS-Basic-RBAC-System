export interface Role {
  id: number;
  role_name: string;
  parent_id: number | null;
  created_at: Date;
}

export interface RoleCreate {
  role_name: string;
  parent_id?: number | null;
}
