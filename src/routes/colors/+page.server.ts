export const load = (async ({locals}) => {
	const { data: colors } = await locals.supabase.from('colors').select('*');
	return { colors: colors ?? [] };
})
