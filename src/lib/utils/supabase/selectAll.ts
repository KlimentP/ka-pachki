import { supabaseClient } from "$lib/supabaseClient";
import type { Database } from '../../../supabase';

type TableName = keyof Database['public']['Tables']

export async function selectAll(
    table: TableName,
  ): Promise<Database['public']['Tables'][TableName]['Row'][]> {
    const { data } = await supabaseClient
      .from(table)
      .select("*");
  
    return data ?? [];
  }
