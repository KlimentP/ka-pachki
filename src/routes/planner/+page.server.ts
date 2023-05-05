import { supabaseClient } from '$lib/supabaseClient';

export async function load() {
	const { data: orders } = await supabaseClient.from('orders_full').select('*');
  const {data: employees} = await supabaseClient.from('employees').select('name,id')  
	return { orders: orders ?? [],
           employees: employees?? [] };
}
