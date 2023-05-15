import { superValidate } from 'sveltekit-superforms/server';
import { customersInsertSchema } from '../../../schemas';
import { handleCreateSubmit } from '$lib/utils/forms/handleCreateSubmit';

const resourceType = 'customers';
const defaultHandle = handleCreateSubmit(customersInsertSchema, resourceType)
export async function load() {
	const form = superValidate(customersInsertSchema);
	return {form, resourceType };
}


/** @type {import('./$types').Actions} */
export const actions = {
	default: defaultHandle,
};
