<script lang="ts">
	import { Auth } from '@supabase/auth-ui-svelte';
	import { page } from '$app/stores';
	import { ThemeSupa } from '@supabase/auth-ui-shared';
</script>

<div class="container h-full mx-auto flex flex-col justify-center align-middle  items-center gap-2">
	<div class="text-sm text-slate-800 w-56 self-center">
		Not registered? <br>Signup bellow and get in touch to activate your account 💌
	</div>
	<div class="flex-center flex">
		<Auth
			supabaseClient={$page.data.supabase}
			view="sign_up"
			redirectTo={`${$page.data.url}/logging-in?redirect=/`}
			showLinks={true}
			appearance={{ theme: ThemeSupa }}
		/>
	</div>
</div>
