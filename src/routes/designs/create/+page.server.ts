import { superValidate } from 'sveltekit-superforms/server';
import { designsInsertSchema } from '../../../schemas';
import { handleCreateSubmit } from '$lib/utils/forms/handleCreateSubmit';

const resourceType = 'designs';
const defaultHandle = handleCreateSubmit(designsInsertSchema, resourceType);

export async function load({ locals }) {
	const { data: machines } = await locals.supabase.from('machines').select('*');
	const { data: colors } = await locals.supabase.from('color_options').select('*');
	console.log(colors);
	const newColors = colors?.map((color) => ({ id: color.name, name: color.name }));
	const form = superValidate(designsInsertSchema);
	return { machines: machines ?? [], colors: newColors ?? [], form };
}
/** @type {import('./$types').Actions} */
export const actions = {
	default: defaultHandle
};
