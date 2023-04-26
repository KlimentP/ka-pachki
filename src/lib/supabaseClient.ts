
import { createClient } from '@supabase/supabase-js'
import { env } from '$env/dynamic/public';
import type { Database } from '../supabase';

export const supabaseClient = createClient<Database>(env.PUBLIC_SUPABASE_URL, env.PUBLIC_SUPABASE_ANON_KEY);