import { handleDelete } from '$lib/utils/forms/handleDelete';
const resource = 'designs';
const deleteDesign = handleDelete(resource);

export async function load({ locals }) {
	const { supabase } = locals;
    const {data} = await supabase
    .from(resource)
    .select('*, machines (name)' )
    return {tableData: data ?? [],};
}

export const actions = {
  deleteDesign
};
