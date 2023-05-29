export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json }
  | Json[]

export interface Database {
  public: {
    Tables: {
      colors: {
        Row: {
          code: string | null
          name: string
        }
        Insert: {
          code?: string | null
          name: string
        }
        Update: {
          code?: string | null
          name?: string
        }
      }
      customers: {
        Row: {
          id: number
          name: string
          notes: string | null
        }
        Insert: {
          id?: number
          name: string
          notes?: string | null
        }
        Update: {
          id?: number
          name?: string
          notes?: string | null
        }
      }
      designs: {
        Row: {
          color_scheme: string[]
          id: number
          material: string
          name: string
          notes: string | null
          preferred_machine_id: number | null
        }
        Insert: {
          color_scheme: string[]
          id?: number
          material: string
          name: string
          notes?: string | null
          preferred_machine_id?: number | null
        }
        Update: {
          color_scheme?: string[]
          id?: number
          material?: string
          name?: string
          notes?: string | null
          preferred_machine_id?: number | null
        }
      }
      designs_bup: {
        Row: {
          color_scheme: string[] | null
          id: number | null
          material: string | null
          name: string | null
          preferred_employee_id: number | null
        }
        Insert: {
          color_scheme?: string[] | null
          id?: number | null
          material?: string | null
          name?: string | null
          preferred_employee_id?: number | null
        }
        Update: {
          color_scheme?: string[] | null
          id?: number | null
          material?: string | null
          name?: string | null
          preferred_employee_id?: number | null
        }
      }
      employees: {
        Row: {
          default_machine: number | null
          id: number
          name: string
        }
        Insert: {
          default_machine?: number | null
          id?: number
          name: string
        }
        Update: {
          default_machine?: number | null
          id?: number
          name?: string
        }
      }
      machines: {
        Row: {
          id: number
          name: string | null
        }
        Insert: {
          id?: number
          name?: string | null
        }
        Update: {
          id?: number
          name?: string | null
        }
      }
      orders: {
        Row: {
          assigned_machine_id: number | null
          closed_by: string | null
          created_by: string
          customer_id: number | null
          date_closed: string | null
          date_created: string | null
          date_updated: string | null
          deadline: string | null
          design_id: number | null
          duration_order: number | null
          id: string
          notes: string | null
          quantity: number | null
          status: string | null
          units_already_produced: number
          urgent: boolean
        }
        Insert: {
          assigned_machine_id?: number | null
          closed_by?: string | null
          created_by: string
          customer_id?: number | null
          date_closed?: string | null
          date_created?: string | null
          date_updated?: string | null
          deadline?: string | null
          design_id?: number | null
          duration_order?: number | null
          id?: string
          notes?: string | null
          quantity?: number | null
          status?: string | null
          units_already_produced?: number
          urgent?: boolean
        }
        Update: {
          assigned_machine_id?: number | null
          closed_by?: string | null
          created_by?: string
          customer_id?: number | null
          date_closed?: string | null
          date_created?: string | null
          date_updated?: string | null
          deadline?: string | null
          design_id?: number | null
          duration_order?: number | null
          id?: string
          notes?: string | null
          quantity?: number | null
          status?: string | null
          units_already_produced?: number
          urgent?: boolean
        }
      }
      orders_bup: {
        Row: {
          assigned_employee_id: number | null
          closed_by: string | null
          created_by: string | null
          customer_id: number | null
          date_closed: string | null
          date_created: string | null
          date_updated: string | null
          deadline: string | null
          design_id: number | null
          duration_order: number | null
          id: string | null
          notes: string | null
          quantity: number | null
          status: string | null
          units_already_produced: number | null
          urgent: boolean | null
        }
        Insert: {
          assigned_employee_id?: number | null
          closed_by?: string | null
          created_by?: string | null
          customer_id?: number | null
          date_closed?: string | null
          date_created?: string | null
          date_updated?: string | null
          deadline?: string | null
          design_id?: number | null
          duration_order?: number | null
          id?: string | null
          notes?: string | null
          quantity?: number | null
          status?: string | null
          units_already_produced?: number | null
          urgent?: boolean | null
        }
        Update: {
          assigned_employee_id?: number | null
          closed_by?: string | null
          created_by?: string | null
          customer_id?: number | null
          date_closed?: string | null
          date_created?: string | null
          date_updated?: string | null
          deadline?: string | null
          design_id?: number | null
          duration_order?: number | null
          id?: string | null
          notes?: string | null
          quantity?: number | null
          status?: string | null
          units_already_produced?: number | null
          urgent?: boolean | null
        }
      }
    }
    Views: {
      color_options: {
        Row: {
          name: string | null
        }
      }
      orders_full: {
        Row: {
          assigned_machine_id: number | null
          closed_by: string | null
          closed_by_email: string | null
          color_scheme: string[] | null
          created_by: string | null
          created_by_email: string | null
          customer_id: number | null
          customer_name: string | null
          date_closed: string | null
          date_created: string | null
          date_updated: string | null
          deadline: string | null
          design_id: number | null
          design_name: string | null
          duration_order: number | null
          id: string | null
          machine: string | null
          material: string | null
          notes: string | null
          quantity: number | null
          status: string | null
          units_already_produced: number | null
          urgent: boolean | null
        }
      }
    }
    Functions: {
      lower_array: {
        Args: {
          input: string[]
        }
        Returns: unknown
      }
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}
