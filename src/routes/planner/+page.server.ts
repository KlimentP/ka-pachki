
export async function load({ locals }) {
	const { data: orders } = await locals.supabase.from('orders_full').select('*');
	const { data: employees } = await locals.supabase.from('employees').select('name,id');
	return { orders: orders ?? [], employees: employees ?? [] };
}
