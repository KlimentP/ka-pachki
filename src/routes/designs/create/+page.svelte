<script lang="ts">
	import AutoCompleteMulti from '$lib/components/AutoCompleteMulti.svelte';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import { fade } from 'svelte/transition';
	import { superForm } from 'sveltekit-superforms/client';
	import { page } from '$app/stores';

	import { dbToAutocomplete } from '$lib/utils/generic';
	export let data;
	let { form, errors, constraints, enhance, delayed, message, empty, reset } = superForm(data.form, {
		onUpdated({ form }) {
			// Need to do this because messages can't be preserved on redirect.
			// sveltekit-flash-message fixes this issue:
			// https://github.com/ciscoheat/sveltekit-flash-message
			if (form.valid) {
				reset({ keepMessage: true });
			}
		}
	});
	// export let form;

	let employeeOptions: AutocompleteOption[] = dbToAutocomplete(data.employees);
	let colorOptions: AutocompleteOption[] = dbToAutocomplete(data.colors);
</script>

<div class="container h-full mx-auto flex flex-col gap-2 justify-center items-center max-sm:p-4">
	<h2 class="">{empty ? 'Create' : 'Update'} Design</h2>
	<!-- TODO put something went wrong after done testing -->

	<form class="form w-full max-w-lg" method="POST" use:enhance>
		<!-- <div class="flex flex-wrap py-4">
		  <div class="w-full px-3">
			<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="design-id">
			  Design ID
			</label>
			<input class="appearance-none block w-full bg-sky-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id="design-id" type="text" placeholder="Design ID">
		  </div>
		</div> -->
		<div class="flex flex-wrap py-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="design-name"
				>
					Design Name
				</label>
				<input
					class="input"
					name="name"
					type="text"
					placeholder="Design Name"
					bind:value={$form.name}
					data-invalid={$errors.name}
					{...$constraints.name}
				/>
			</div>
			{#if $errors.name}<span class="text-error-500">{$errors.name}</span>{/if}
		</div>
		<div class="flex flex-wrap py-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="color-scheme"
				>
					Color Scheme
				</label>
				<AutoCompleteMulti form={$form} options={colorOptions} formName="color_scheme" />
			</div>
			{#if $errors.color_scheme}<span class="text-error-500">{$errors.color_scheme}</span>{/if}
		</div>
		<div class="flex flex-wrap py-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Material
				</label>
				<select
					class="select"
					name="material"
					size="3"
					bind:value={$form.material}
					data-invalid={$errors.material}
					{...$constraints.material}
				>
					<option value="lid">Lid</option>
					<option value="label">Label</option>
					<option value="butter">Butter</option>
					<option value="uv_butter">UV Butter</option>
					<option value="embossed_lids">Embossed Lid</option>
				</select>
			</div>
			{#if $errors.material}<span class="text-error-500">{$errors.material}</span>{/if}
		</div>
		<div class="flex flex-wrap py-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Preferred Employee
				</label>
				<select
					class="select"
					name="preferred_employee_id"
					size="3"
					bind:value={$form.preferred_employee_id}
					data-invalid={$errors.preferred_employee_id}
					{...$constraints.preferred_employee_id}
				>
					{#each employeeOptions as employee}
						<option value={employee.value}>{employee.label}</option>
					{/each}
				</select>
			</div>
			{#if $errors.preferred_employee_id}<span class="text-error-500"
					>{$errors.preferred_employee_id}</span
				>{/if}
		</div>
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
		<div class="flex flex-wrap -mx-3 my-2">
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
