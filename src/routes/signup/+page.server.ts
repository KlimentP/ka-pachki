import { fail } from '@sveltejs/kit';

export const actions = {
	default: async ({ request, locals: { supabase } }) => {
		const formData = await request.formData();
		const email = formData.get('email') as string;
		const password = formData.get('password') as string;

		const { error } = await supabase.auth.signUp({
			email,
			password
		});
		if (error) {
			console.log(error.message);
			return fail(400, { error: error.message, success: false, email });
		}
		return { message: 'Get in touch to get your account activated', success: true, email };
	}
};
