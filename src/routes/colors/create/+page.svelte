<script lang="ts">
	import { superForm } from 'sveltekit-superforms/client';
	import { page } from '$app/stores';
	import { fade } from 'svelte/transition';

	export let data;
	let { form, errors, constraints, enhance, delayed, message, empty, reset } = superForm(
		data.form,
		{
			onUpdated({ form }) {
				// Need to do this because messages can't be preserved on redirect.
				// sveltekit-flash-message fixes this issue:
				// https://github.com/ciscoheat/sveltekit-flash-message
				if (form.valid) {
					reset({ keepMessage: true });
				}
			}
		}
	);
</script>

<div class="container h-full mx-auto flex flex-col gap-2 justify-center items-center max-sm:p-4">
	<h2 class="">{empty ? 'Create' : 'Update'} {data.resourceType}</h2>

	<form class="form w-full max-w-lg" method="POST" use:enhance>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="color-name"
				>
					Color Name
				</label>
				<input
					class="input"
					name="name"
					type="text"
					placeholder="Color Name"
					bind:value={$form.name}
					data-invalid={$errors.name}
					{...$constraints.name}
				/>
			</div>
			{#if $errors.name}<span class="text-error-500">{$errors.name}</span>{/if}
		</div>
		<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="notes">
			Color Code
		</label>
		<div class="grid grid-cols-[auto_1fr] gap-2 -mx-3 mb-6">
			<input class="input" type="color" bind:value={$form.code} />
			<input
				class="input"
				type="text"
				name="code"
				bind:value={$form.code}
				{...$constraints.code}
				readonly
				tabindex="-1"
			/>
		</div>
		<!-- <div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="notes"
				>
					Color Code
				</label>
				<textarea
					class="textarea"
					id="notes"
					name="notes"
					bind:value={$form.notes}
					{...$constraints.notes}
				/>
			</div>
		</div> -->
		{#if Object.keys($errors).length > 0}
		<aside class="alert variant-filled-error p-4" transition:fade|local={{ duration: 500 }}>
			{JSON.stringify($errors)}
		</aside>
	{/if}
		{#if $message}
			<aside
				transition:fade|local={{ duration: 500 }}
				class="alert"
				class:variant-filled-success={$page.status < 400}
				class:variant-filled-error={$page.status >= 400}
			>
				<h3>{$message}</h3>
			</aside>
		{/if}
		<div class="flex flex-wrap -mx-3 mb-2">
			<div class="w-full px-3">
				<button
					class="bg-primary-500 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
					type="submit"
				>
					Submit
				</button>
			</div>
		</div>
	</form>
</div>
