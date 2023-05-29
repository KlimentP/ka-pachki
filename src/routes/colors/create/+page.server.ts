import { superValidate } from 'sveltekit-superforms/server';
import { colorsInsertSchema } from '../../../schemas';
import { handleCreateSubmit } from '$lib/utils/forms/handleCreateSubmit';

const resourceType = 'colors';
const defaultHandle = handleCreateSubmit(colorsInsertSchema, resourceType);
export async function load() {
	const form = superValidate(colorsInsertSchema);
	return { form, resourceType };
}
/** @type {import('./$types').Actions} */
export const actions = {
	default: defaultHandle
};