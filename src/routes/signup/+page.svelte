<script lang="ts">
	import { Auth } from '@supabase/auth-ui-svelte';
	import { page } from '$app/stores';
	import { ThemeSupa } from '@supabase/auth-ui-shared';
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center gap-2">
	<div class="row flex-center flex">
		<Auth
			supabaseClient={$page.data.supabase}
			view="sign_up"
			redirectTo={`${$page.data.url}/logging-in?redirect=/`}
			showLinks={true}
			appearance={{ theme: ThemeSupa }}
		/>
	</div>
</div>
