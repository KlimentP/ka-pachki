import { fail } from '@sveltejs/kit';
import { message, setError, superValidate } from 'sveltekit-superforms/server';
import { designsInsertSchema } from '../../../schemas';
import { removeNullValues } from '$lib/utils/generic';

export async function load({locals}) {

	const { data: employees } = await locals.supabase.from('employees').select('*');
	const { data: colors } = await locals.supabase.from('colors').select('*');
	const newColors = colors?.map((color) => ({ id: color.name, name: color.name }));
	const form = superValidate(designsInsertSchema);
	return { employees: employees ?? [], colors: newColors ?? [], form };
}

// const validate = (submitData: any) => {
//     const errors: any = {};
//     if (submitData.color_scheme.length < 2) {
//         errors.color_scheme = 'Please select at least 2 or more colors';
//     }
//     return errors;
// }

/** @type {import('./$types').Actions} */
export const actions = {
	default: async ({ request, locals }) => {
		// const formData = await request.formData();
		const form = await superValidate(request, designsInsertSchema);
		if (!form.valid) return fail(400, { form });
        const submitData = removeNullValues(form.data)
		if (!form.data.id) {
            // CREATE DESIGN
			const { error } = await locals.supabase.from('designs').insert([submitData]);
			if (error) {
				return setError(form, null, error.message);
			}
			return message(form, 'Design created!');
		} else {
            // UPDATE DESIGN
            const { error } = await locals.supabase.from('designs').update(submitData).eq("id", form.data.id );
            if (error) {
                return setError(form, null, error.message);
            }
            return message(form, 'Design updated!');
        }
	}
};

// /** @type {import('./$types').Actions} */
// export const actions = {
//     default: async ({request, locals})  => {
//         const formData = await request.formData();
//         const submitData = {color_scheme: []};
//         for (const [key, value] of formData.entries()) {
//             if (key === 'color_scheme') {
//                 submitData[key].push(value);
//             }
//             else {
//                 submitData[key] = value;
//             }
//         }

//         if (Object.keys(errors).length > 0) {
//             return fail(422, {...submitData, errors});
//         }
//         const {error} = await locals.supabase.from('designs').insert([submitData]);
//         if (error) {
//             return fail(422, {...submitData, errors: [error]});
//         }
//         throw(redirect(303, '/designs'))
//     }
// };
