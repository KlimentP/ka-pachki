
import  {selectOrders} from '$lib/utils/supabase/selectOrders';

export async function load({ locals }) {
	const orders = await selectOrders();
	const { data: employees } = await locals.supabase.from('employees').select('name,id,machines(id, name)');
	// const { data: machinesResp } = await locals.supabase.from('machines').select('name');
	// const machines = machinesResp?.map((machine) => machine.name);
	return { 
		orders: orders ?? [], 
		employees: employees ?? [], 
		// machines: machines ?? [] 
	};
}
