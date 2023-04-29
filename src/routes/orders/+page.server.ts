import { supabaseClient } from '$lib/supabaseClient';

export async function load() {
	const { data } = await supabaseClient.from('orders_full').select('*');
	return { tableData: data ?? [] };
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
  }
};
