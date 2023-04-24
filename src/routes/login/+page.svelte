<script lang="ts">
	import { Auth } from '@supabase/auth-ui-svelte';
	import { page } from '$app/stores';
	import { ThemeSupa } from '@supabase/auth-ui-shared';
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center gap-2">
	<div class="row flex-center flex">
		<div class="col-6 text-slate-600 rounded-lg">
			
			<Auth
				supabaseClient={$page.data.supabase}
				view="sign_in"
				redirectTo={`/logging-in?redirect=/`}
				showLinks={false}
				appearance={{theme: ThemeSupa}}
				/>
		</div>
	</div>
    <a href="/signup">Not registered? Sign up here</a>
</div>
