/** @type {import('./$types').Actions} */
import { superValidate } from 'sveltekit-superforms/server';
import { ordersInsertSchema } from '../../../schemas';
import { handleCreateSubmit } from '$lib/utils/forms/handleCreateSubmit';

const resourceType = 'orders';
const defaultHandle = handleCreateSubmit(ordersInsertSchema, resourceType, true)

export async function load({ locals }) {
	const { data: employees } = await locals.supabase.from('employees').select('name, id');
	const { data: designs } = await locals.supabase.from('designs').select('name,id');
	const { data: customers } = await locals.supabase.from('customers').select('name,id');
	const form = superValidate(ordersInsertSchema);

	return { employees: employees ?? [], designs: designs ?? [], customers: customers ?? [], form };
}

export const actions = {
	default: defaultHandle
};
