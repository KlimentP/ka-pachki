import { supabaseClient } from "$lib/supabaseClient";

// import { selectAll } from "$lib/utils/supabase/selectAll";
export async function load() {
    const {data} = await supabaseClient
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
        console.log(error)
      return {error: error.message};
  }
  return {message: 'Success'};
  }
};
