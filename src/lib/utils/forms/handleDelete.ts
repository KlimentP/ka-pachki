import { handleModalFormErrors } from "./generic";

export const handleDelete = (resource: string) => {
    return async ({ request, locals }) => {
        const data = await request.formData();
        const { error } = await locals.supabase.from(resource).delete().eq('id', data.get('id'));
        handleModalFormErrors(error);
    }
}