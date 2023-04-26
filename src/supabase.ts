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
      designs: {
        Row: {
          color_scheme: string[]
          id: number
          material: string
          name: string
          preferred_employee: number | null
        }
        Insert: {
          color_scheme: string[]
          id?: number
          material: string
          name: string
          preferred_employee?: number | null
        }
        Update: {
          color_scheme?: string[]
          id?: number
          material?: string
          name?: string
          preferred_employee?: number | null
        }
      }
      employees: {
        Row: {
          id: number
          name: string
        }
        Insert: {
          id?: number
          name: string
        }
        Update: {
          id?: number
          name?: string
        }
      }
      orders: {
        Row: {
          closed_by: string | null
          created_by: string | null
          customer_id: string | null
          date_closed: string | null
          date_created: string | null
          date_updated: string | null
          deadline: string | null
          design_id: number | null
          duration_order: number | null
          notes: string | null
          order_id: string
          quantity: number | null
          status: string | null
          units_already_produced: number
          urgent: boolean
        }
        Insert: {
          closed_by?: string | null
          created_by?: string | null
          customer_id?: string | null
          date_closed?: string | null
          date_created?: string | null
          date_updated?: string | null
          deadline?: string | null
          design_id?: number | null
          duration_order?: number | null
          notes?: string | null
          order_id?: string
          quantity?: number | null
          status?: string | null
          units_already_produced?: number
          urgent?: boolean
        }
        Update: {
          closed_by?: string | null
          created_by?: string | null
          customer_id?: string | null
          date_closed?: string | null
          date_created?: string | null
          date_updated?: string | null
          deadline?: string | null
          design_id?: number | null
          duration_order?: number | null
          notes?: string | null
          order_id?: string
          quantity?: number | null
          status?: string | null
          units_already_produced?: number
          urgent?: boolean
        }
      }
    }
    Views: {
      orders_full: {
        Row: {
          closed_by: string | null
          color_scheme: string[] | null
          created_by: string | null
          created_by_email: string | null
          customer_id: string | null
          date_closed: string | null
          date_created: string | null
          date_updated: string | null
          deadline: string | null
          design_id: number | null
          duration_order: number | null
          id: number | null
          material: string | null
          name: string | null
          notes: string | null
          order_id: string | null
          preferred_emplopyee: number | null
          quantity: number | null
          status: string | null
          units_already_produced: number | null
          urgent: boolean | null
        }
      }
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}