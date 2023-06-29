<script lang="ts">
	import { enhance } from '$app/forms';
	export let form;
</script>

<div class="container h-full mx-auto flex flex-col justify-center align-middle  items-center gap-2">
	<div class="text-sm text-slate-800 w-56 self-center">
		Not registered? <br>Signup bellow and get in touch to activate your account 💌
	</div>
	<form class="form flex flex-col gap-4" method="post" use:enhance>
		<div>
			<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="email">
				Email
			</label>

			<input class="input" type="text" name="email" value={form?.email ?? ''} />
		</div>
		<div>
			<label
				class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
				for="password"
			>
				Password
			</label>
			<input class="input" type="password" name="password" />
		</div>
		<button
			class="bg-primary-500 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
			type="submit"
			>Sign Up
		</button>
		{#if form?.error}
			<div class="alert variant-filled-error">
				{form?.error}
			</div>
		{/if}
		{#if form?.message}
		<div class="alert variant-filled-success">
			{form?.message}
		</div>
	{/if}
	</form>
</div>
