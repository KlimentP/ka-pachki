export async function load({ locals }) {
	const { supabase } = locals;
    const {data} = await supabase
    .from('designs')
    .select('*, employees (name)' )
    return {tableData: data ?? [],};
}

export const actions = {
  deleteDesign : async ({ request, locals }) => {
    const data = await request.formData();
    const { error } =  await  locals.supabase
    .from('designs')
    .delete()
    .eq('id', data.get('id'));
    if (error) {
      return {error: error.message};
  }
  return {message: 'Success'};
  }
};
