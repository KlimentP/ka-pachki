import { supabaseClient } from "$lib/supabaseClient";

// import { selectAll } from "$lib/utils/supabase/selectAll";
export async function load() {
    const {data} = await supabaseClient
    .from('designs')
    .select('*, employees (name)' )
    return {tableData: data ?? [],};
}