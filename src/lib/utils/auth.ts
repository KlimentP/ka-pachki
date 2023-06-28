import { invalidateAll } from '$app/navigation';


export async function signOut(supabase) {
    supabase.auth.signOut()
    invalidateAll()
}
