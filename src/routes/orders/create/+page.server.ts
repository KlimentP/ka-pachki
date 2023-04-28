/** @type {import('./$types').Actions} */
import { fail, redirect } from '@sveltejs/kit';
import { supabaseClient } from "$lib/supabaseClient";

export async function load(){
    const {data: employees} =  await supabaseClient.from('employees').select('*')
    const {data: designs} =  await supabaseClient.from('designs').select('name,id')
    const {data: customers} =  await supabaseClient.from('customers').select('name,id')

    return {employees: employees ?? [],
            designs: designs ?? [],
            customers: customers ?? [],
            };
}

const validate = (submitData: any) => {
    const errors: any = {};
    if (new Date(submitData?.deadline).setHours(0,0,0,0) < new Date().setHours(0,0,0,0) ){
        errors.deadline = 'Please select a date in the future';
    }
    if (submitData?.quantity <= 0){
        errors.quantity = 'Please enter a valid number';
    }
    if (submitData?.units_already_produced < 0){
        errors.units_already_produced = 'Please enter a valid number';
    }
    return errors;
} 


export const actions = {
    default: async ({request, locals}) => {
        const formData = await request.formData();
        const session = await locals.getSession()
        const creator = {created_by: session?.user.id}
        const submitData = {...Object.fromEntries(formData.entries()), ...creator}

        const errors = validate(submitData);
        if (Object.keys(errors).length > 0) {
            return fail(422, {...submitData, errors});
        }

        const {error} = await locals.supabase.from('orders').insert([submitData]);
            if (error) {
                return fail(422, {...submitData, errors: error});
            }
            throw(redirect(303, '/orders'))
        }
    };
