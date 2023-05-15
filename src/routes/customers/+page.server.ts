import { handleDelete } from '$lib/utils/forms/handleDelete';
const resource = 'customers';
const deleteCustomer = handleDelete(resource);

export async function load({ locals }) {
	const { data } = await locals.supabase
		.from(resource)
		.select(
			'id, name, orders (id,  status, deadline, quantity, units_already_produced, urgent, designs(name))'
		);
	return { tableData: data ?? [] };
}

export const actions = {
	deleteCustomer
};
