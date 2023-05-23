import { message, setError, superValidate } from 'sveltekit-superforms/server';
import { removeNullValues, capitalizeString } from '$lib/utils/generic';
import { error, fail } from '@sveltejs/kit';

export const handleCreateSubmit = (schema: any, resource: string, withCreator = false) => {
	return async ({ request, locals: { supabase, getSession } }) => {
		const session = await getSession();
		if (!session) {
			// the user is not signed in
			throw error(401, { message: 'Unauthorized' });
		}
		const form = await superValidate(request, schema);
		if (!form.valid) {
			return fail(400, { form });
		}
		let submitData = removeNullValues(form.data);
		if (withCreator) {
			const session = await getSession();
			const creator = { created_by: session?.user.id };
			submitData = { ...submitData, ...creator };
		}
		if (!form.data.id) {
			// CREATE
			const { error } = await supabase.from(resource).insert([submitData]);
			if (error) {
				return setError(form, null, error.message);
			}
			return message(form, `${capitalizeString(resource)} created!`);
		} else {
			// UPDATE
			const { error } = await supabase.from(resource).update(submitData).eq('id', form.data.id);
			if (error) {
				return setError(form, null, error.message);
			}
			return message(form, `${capitalizeString(resource)} updated!`);
		}
	};
};
