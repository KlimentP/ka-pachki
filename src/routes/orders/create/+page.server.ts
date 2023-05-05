/** @type {import('./$types').Actions} */
import { fail } from '@sveltejs/kit';
import { supabaseClient } from '$lib/supabaseClient';
import { message, setError, superValidate } from 'sveltekit-superforms/server';
import { ordersInsertSchema } from '../../../schemas';
import { removeNullValues } from '$lib/utils/generic';

export async function load() {
	const { data: employees } = await supabaseClient.from('employees').select('*');
	const { data: designs } = await supabaseClient.from('designs').select('name,id');
	const { data: customers } = await supabaseClient.from('customers').select('name,id');
	const form = superValidate(ordersInsertSchema);

	return { employees: employees ?? [], designs: designs ?? [], customers: customers ?? [], form };
}

export const actions = {
	default: async ({ request, locals }) => {
		const form = await superValidate(request, ordersInsertSchema);
		console.log(form);
		if (!form.valid) return fail(400, { form });
		let submitData = removeNullValues(form.data);
		const session = await locals.getSession();
		const creator = { created_by: session?.user.id };
		submitData = { ...submitData, ...creator };
		if (!form.data.id) {
			// CREATE order
			const { error } = await locals.supabase.from('orders').insert([submitData]);
			if (error) {
				return setError(form, null, error.message);
			}
			return message(form, 'Order created!');
		} else {
			// UPDATE order
			const { error } = await locals.supabase
				.from('orders')
				.update(submitData)
				.eq('id', form.data.id);
			if (error) {
				return setError(form, null, error.message);
			}
			return message(form, 'Order updated!');
		}
	}
};
