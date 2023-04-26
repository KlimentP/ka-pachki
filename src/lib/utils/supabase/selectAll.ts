import { supabaseClient } from "$lib/supabaseClient";

export async function selectAll(table: string) {
    const {data} = await supabaseClient
    .from(table)
    .select()
  return {
    tableData: data ?? [],
  };
}