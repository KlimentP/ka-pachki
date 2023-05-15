
import  {selectOrders} from '$lib/utils/supabase/selectOrders';

export async function load({ locals }) {
	const orders = await selectOrders();
	const { data: employees } = await locals.supabase.from('employees').select('name,id');
	return { orders: orders ?? [], employees: employees ?? [] };
}
