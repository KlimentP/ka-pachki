import { handleModalFormErrors } from "./generic";
import { error } from '@sveltejs/kit';

export const handleDelete = (resource: string) => {
    return async ({ request, locals: { supabase, getSession } }) => {
        const session = await getSession()
        if (!session) {
            // the user is not signed in
            throw error(401, { message: 'Unauthorized' })
          }
        const data = await request.formData();
        const { err } = await supabase.from(resource).delete().eq('id', data.get('id'));
        handleModalFormErrors(err);
    }
}