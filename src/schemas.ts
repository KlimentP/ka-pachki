// Generated by ts-to-zod
import { z } from 'zod';
import type { Json } from './supabase';

export const jsonSchema: z.ZodSchema<Json> = z.lazy(() =>
	z
		.union([z.string(), z.number(), z.boolean(), z.record(jsonSchema), z.array(jsonSchema)])
		.nullable()
);

export const colorsRowSchema = z.object({
	name: z.string()
});

export const colorsInsertSchema = z.object({
	name: z.string()
});

export const colorsUpdateSchema = z.object({
	name: z.string().optional()
});

export const customersRowSchema = z.object({
	id: z.number(),
	name: z.string(),
	notes: z.string().nullable()
});

export const customersInsertSchema = z.object({
	id: z.number().optional(),
	name: z.string(),
	notes: z.string().optional().nullable()
});

export const customersUpdateSchema = z.object({
	id: z.number().optional(),
	name: z.string().optional(),
	notes: z.string().optional().nullable()
});

export const designsRowSchema = z.object({
	color_scheme: z.array(z.string()),
	id: z.number(),
	material: z.string(),
	name: z.string(),
	preferred_employee_id: z.number().nullable()
});

export const designsInsertSchema = z.object({
	color_scheme: z.array(z.string() ).min(2).max(6),
	id: z.number().optional(),
	material: z.string(),
	name: z.string(),
	preferred_employee_id: z.number().optional().nullable()
});

export const designsUpdateSchema = z.object({
	color_scheme: z.array(z.string()).optional(),
	id: z.number().optional(),
	material: z.string().optional(),
	name: z.string().optional(),
	preferred_employee_id: z.number().optional().nullable()
});

export const employeesRowSchema = z.object({
	id: z.number(),
	name: z.string()
});

export const employeesInsertSchema = z.object({
	id: z.number().optional(),
	name: z.string()
});

export const employeesUpdateSchema = z.object({
	id: z.number().optional(),
	name: z.string().optional()
});

export const ordersRowSchema = z.object({
	assigned_employee_id: z.number().nullable(),
	closed_by: z.string().nullable(),
	created_by: z.string().nullable(),
	customer_id: z.number().nullable(),
	date_closed: z.string().nullable(),
	date_created: z.string().nullable(),
	date_updated: z.string().nullable(),
	deadline: z.string().nullable(),
	design_id: z.number().nullable(),
	duration_order: z.number().nullable(),
	notes: z.string().nullable(),
	order_id: z.string(),
	quantity: z.number().nullable(),
	status: z.string().nullable(),
	units_already_produced: z.number(),
	urgent: z.boolean()
});

export const ordersInsertSchema = z.object({
	assigned_employee_id: z.number().optional().nullable(),
	closed_by: z.string().optional().nullable(),
	created_by: z.string().optional().nullable(),
	customer_id: z.number().optional().nullable(),
	date_closed: z.string().optional().nullable(),
	date_created: z.string().optional().nullable(),
	date_updated: z.string().optional().nullable(),
	deadline: z.string().optional().nullable(),
	design_id: z.number().optional().nullable(),
	duration_order: z.number().optional().nullable(),
	notes: z.string().optional().nullable(),
	order_id: z.string().optional(),
	quantity: z.number().optional().nullable(),
	status: z.string().optional().nullable().default('scheduled'),
	units_already_produced: z.number().optional(),
	urgent: z.boolean().optional()
});

export const ordersUpdateSchema = z.object({
	assigned_employee_id: z.number().optional().nullable(),
	closed_by: z.string().optional().nullable(),
	created_by: z.string().optional().nullable(),
	customer_id: z.number().optional().nullable(),
	date_closed: z.string().optional().nullable(),
	date_created: z.string().optional().nullable(),
	date_updated: z.string().optional().nullable(),
	deadline: z.string().optional().nullable(),
	design_id: z.number().optional().nullable(),
	duration_order: z.number().optional().nullable(),
	notes: z.string().optional().nullable(),
	order_id: z.string().optional(),
	quantity: z.number().optional().nullable(),
	status: z.string().optional().nullable(),
	units_already_produced: z.number().optional(),
	urgent: z.boolean().optional()
});

export const ordersFullRowSchema = z.object({
	assigned_employee_id: z.number().nullable(),
	closed_by: z.string().nullable(),
	closed_by_email: z.string().nullable(),
	color_scheme: z.array(z.string()).nullable(),
	creaated_by_email: z.string().nullable(),
	created_by: z.string().nullable(),
	customer_id: z.number().nullable(),
	customer_name: z.string().nullable(),
	date_closed: z.string().nullable(),
	date_created: z.string().nullable(),
	date_updated: z.string().nullable(),
	deadline: z.string().nullable(),
	design_id: z.number().nullable(),
	design_name: z.string().nullable(),
	duration_order: z.number().nullable(),
	material: z.string().nullable(),
	notes: z.string().nullable(),
	order_id: z.string().nullable(),
	preferred_employee_id_name: z.string().nullable(),
	quantity: z.number().nullable(),
	status: z.string().nullable(),
	units_already_produced: z.number().nullable(),
	urgent: z.boolean().nullable()
});
