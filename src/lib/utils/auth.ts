import { supabaseClient } from "$lib/supabaseClient"


export async function signOut() {
    try {
        const { error } = await supabaseClient.auth.signOut()
        if (error) throw error
    } catch (error) {
        if (error instanceof Error) {
            alert(error.message)
        }
    }
}
