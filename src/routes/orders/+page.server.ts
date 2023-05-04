import { supabaseClient } from '$lib/supabaseClient';

export async function load() {
	const { data } = await supabaseClient.from('orders_full').select('*');
  const {data: employees} = await supabaseClient.from('employees').select('name,id')  
	return { tableData: data ?? [],
           employees: employees ?? [] };
}

export const actions = {
	updateStatus: async ({ request, locals }) => {
		const data = await request.formData();
    console.log(data)
		const {error} = await locals.supabase
			.from('orders')
			.update({ status: data.get('status') })
			.eq('order_id', data.get('order_id'));
    console.log(error)
	},
  updateUrgency: async ({ request, locals }) => {
    const data = await request.formData();
    console.log(data)
    await locals.supabase
    .from('orders')
    .update({ urgent: data.get('urgent') })
    .eq('order_id', data.get('order_id'));
  },
  assignEmployee: async ({ request, locals }) => {
    const data = await request.formData();
    await locals.supabase
    .from('orders')
    .update({ assigned_employee_id: data.get('assigned_employee_id') })
    .eq('order_id', data.get('order_id'));
  },
  updateUnitsProduced: async ({ request, locals }) => {
    const data = await request.formData();
    await locals.supabase
    .from('orders')
    .update({ units_already_produced: data.get('units_already_produced'), status: 'in_progress' })
    .eq('order_id', data.get('order_id'));
  },
  deleteOrder : async ({ request, locals }) => {
    const data = await request.formData();
    await locals.supabase
    .from('orders')
    .delete()
    .eq('order_id', data.get('order_id'));
  }

};
