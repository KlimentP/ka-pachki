export type Json = string | number | boolean | null | { [key: string]: Json } | Json[];

export interface Database {
	public: {
		Tables: {
			colors: {
				Row: {
					name: string;
				};
				Insert: {
					name: string;
				};
				Update: {
					name?: string;
				};
			};
			customers: {
				Row: {
					id: number;
					name: string;
					notes: string | null;
				};
				Insert: {
					id?: number;
					name: string;
					notes?: string | null;
				};
				Update: {
					id?: number;
					name?: string;
					notes?: string | null;
				};
			};
			designs: {
				Row: {
					color_scheme: string[];
					id: number;
					material: string;
					name: string;
					preferred_employee_id: number | null;
				};
				Insert: {
					color_scheme: string[];
					id?: number;
					material: string;
					name: string;
					preferred_employee_id?: number | null;
				};
				Update: {
					color_scheme?: string[];
					id?: number;
					material?: string;
					name?: string;
					preferred_employee_id?: number | null;
				};
			};
			employees: {
				Row: {
					id: number;
					name: string;
				};
				Insert: {
					id?: number;
					name: string;
				};
				Update: {
					id?: number;
					name?: string;
				};
			};
			orders: {
				Row: {
					assigned_employee_id: number | null;
					closed_by: string | null;
					created_by: string;
					customer_id: number | null;
					date_closed: string | null;
					date_created: string | null;
					date_updated: string | null;
					deadline: string | null;
					design_id: number | null;
					duration_order: number | null;
					notes: string | null;
					id: string;
					quantity: number | null;
					status: string | null;
					units_already_produced: number;
					urgent: boolean;
				};
				Insert: {
					assigned_employee_id?: number | null;
					closed_by?: string | null;
					created_by: string;
					customer_id?: number | null;
					date_closed?: string | null;
					date_created?: string | null;
					date_updated?: string | null;
					deadline?: string | null;
					design_id?: number | null;
					duration_order?: number | null;
					notes?: string | null;
					id?: string;
					quantity?: number | null;
					status?: string | null;
					units_already_produced?: number;
					urgent?: boolean;
				};
				Update: {
					assigned_employee_id?: number | null;
					closed_by?: string | null;
					created_by?: string;
					customer_id?: number | null;
					date_closed?: string | null;
					date_created?: string | null;
					date_updated?: string | null;
					deadline?: string | null;
					design_id?: number | null;
					duration_order?: number | null;
					notes?: string | null;
					id?: string;
					quantity?: number | null;
					status?: string | null;
					units_already_produced?: number;
					urgent?: boolean;
				};
			};
		};
		Views: {
			orders_full: {
				Row: {
					assigned_employee_id: number | null;
					closed_by: string | null;
					closed_by_email: string | null;
					color_scheme: string[] | null;
					created_by: string | null;
					created_by_email: string | null;
					customer_id: number | null;
					customer_name: string | null;
					date_closed: string | null;
					date_created: string | null;
					date_updated: string | null;
					deadline: string | null;
					design_id: number | null;
					design_name: string | null;
					duration_order: number | null;
					employee: string | null;
					material: string | null;
					notes: string | null;
					id: string | null;
					quantity: number | null;
					status: string | null;
					units_already_produced: number | null;
					urgent: boolean | null;
				};
			};
		};
		Functions: {
			[_ in never]: never;
		};
		Enums: {
			[_ in never]: never;
		};
		CompositeTypes: {
			[_ in never]: never;
		};
	};
}
