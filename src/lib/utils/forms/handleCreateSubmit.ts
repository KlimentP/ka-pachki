
import { message, setError, superValidate } from 'sveltekit-superforms/server';
import { removeNullValues, capitalizeString } from '$lib/utils/generic';
import { fail } from '@sveltejs/kit';

export const handleCreateSubmit = (schema: any, resource: string) => {

    return async ({ request, locals }) => {
    // const formData = await request.formData();
    const form = await superValidate(request, schema);
    if (!form.valid) return fail(400, { form });
    const submitData = removeNullValues(form.data)
    if (!form.data.id) {
        // CREATE
        const { error } = await locals.supabase.from(resource).insert([submitData]);
        if (error) {
            return setError(form, null, error.message);
        }
        return message(form, `${capitalizeString(resource)} created!`);
    } else {
        // UPDATE
        const { error } = await locals.supabase.from(resource).update(submitData).eq("id", form.data.id );
        if (error) {
            return setError(form, null, error.message);
        }
        return message(form, `${capitalizeString(resource)} updated!`);
    }
}}