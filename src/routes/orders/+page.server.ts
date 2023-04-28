import { supabaseClient } from "$lib/supabaseClient";

export async function load () {
  const {data} = await supabaseClient
  .from('orders_full')
  .select("*")
  return {tableData: data ?? [],};
  
}