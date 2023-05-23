import { handleDelete } from '$lib/utils/forms/handleDelete';
import { handleModalFormErrors } from '$lib/utils/forms/generic';

const resource = 'orders';
const deleteOrder = handleDelete(resource);

export async function load({ locals }) {
	const { data } = await locals.supabase.from('orders_full').select('*').order('date_created', { ascending: false });
	const { data: machines } = await locals.supabase.from('machines').select('name,id');
	return { tableData: data ?? [], machines: machines ?? [] };
}

export const actions = {
	updateStatus: async ({ request, locals }) => {
		const data = await request.formData();
		const { error } = await locals.supabase
			.from('orders')
			.update({ status: data.get('status') })
			.eq('id', data.get('id'));
		handleModalFormErrors(error);
	},
	updateUrgency: async ({ request, locals }) => {
		const data = await request.formData();
		const { error } = await locals.supabase
			.from('orders')
			.update({ urgent: data.get('urgent') })
			.eq('id', data.get('id'));
		handleModalFormErrors(error);
	},
	assignMachine: async ({ request, locals }) => {
		const data = await request.formData();
		const { error } = await locals.supabase
			.from('orders')
			.update({ assigned_machine_id: data.get('assigned_machine_id') })
			.eq('id', data.get('id'));
		handleModalFormErrors(error);
	},
	updateUnitsProduced: async ({ request, locals }) => {
		const data = await request.formData();
		const { error } = await locals.supabase
			.from('orders')
			.update({ units_already_produced: data.get('units_already_produced'), status: 'in_progress' })
			.eq('id', data.get('id'));
		handleModalFormErrors(error);
	},
	deleteOrder
};
