/** @type {import('./$types').Actions} */
import { fail, redirect } from '@sveltejs/kit';
import { supabaseClient } from "$lib/supabaseClient";

export async function load(){
    // throw new Error('Not implemented');
    const {data} =  await supabaseClient.from('employees').select('*')
    return {employees: data ?? [],};
}

export const actions = {
    default: async ({request, locals}) => {
        const formData = await request.formData();
        const submitData = {color_scheme: []};
        for (const [key, value] of formData.entries()) {
            if (key === 'color_scheme') {  
                submitData[key].push(value); 
            }
            else {
                submitData[key] = value;
            }
        }
        if (submitData.color_scheme.length < 2) {
            return fail(422, {color_scheme: submitData.color_scheme,
                error: 'Please select at least 2 or more colors'
            });
        }
        const {error} = await locals.supabase.from('designs').insert([submitData]);
        if (error) {
            return fail(422, {error});
        }
        throw(redirect(303, '/designs'))
    }
};