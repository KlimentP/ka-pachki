import { fail, redirect } from '@sveltejs/kit';
import { supabaseClient } from "$lib/supabaseClient";

export async function load(){
    const {data: employees} =  await supabaseClient.from('employees').select('*')
    const {data: colors} =  await supabaseClient.from('colors').select('*')
    const newColors = colors?.map(color => ({id:color.name, name: color.name}) )
    return {employees: employees ?? [],
            colors: newColors ?? [],
        };
} 

const validate = (submitData: any) => {
    const errors: any = {};
    if (submitData.color_scheme.length < 2) {
        errors.color_scheme = 'Please select at least 2 or more colors';
    }
    return errors;
}

/** @type {import('./$types').Actions} */
export const actions = {
    default: async ({request, locals})  => {
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
        const errors = validate(submitData);
        if (Object.keys(errors).length > 0) {
            return fail(422, {...submitData, errors});
        }
        const {error} = await locals.supabase.from('designs').insert([submitData]);
        if (error) {
            return fail(422, {...submitData, errors: [error]});
        }
        throw(redirect(303, '/designs'))
    }
};