import { supabaseClient } from '$lib/supabaseClient';
import { fail } from '@sveltejs/kit';

export async function load() {
	const { data } = await supabaseClient.from('orders_full').select('*');
	return { tableData: data ?? [] };
}

export const actions = {
	updateStatus: async ({ request, locals }) => {
		const data = await request.formData();
		await locals.supabase
			.from('orders')
			.update({ status: data.get('status') })
			.eq('order_id', data.get('order_id'));
	}
};
