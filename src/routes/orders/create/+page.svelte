<script lang="ts">
	import AutoCompleteSingle from '$lib/components/AutoCompleteSingle.svelte';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import { dbToAutocomplete, capitalizeString } from '$lib/utils/generic';
	import { fade } from 'svelte/transition';
	import { superForm } from 'sveltekit-superforms/client';
	import { page } from '$app/stores';
	export let data;
	let resetAutoComplete = false;
	const { form, errors, constraints, message, reset, enhance } = superForm(data.form, {
		onUpdated({ form }) {
			// Need to do this because messages can't be preserved on redirect.
			// sveltekit-flash-message fixes this issue:
			// https://github.com/ciscoheat/sveltekit-flash-message
			if (form.valid ) {
				reset({ keepMessage: true });
				resetAutoComplete = true;
			}
		}
	});
	let customerOptions: AutocompleteOption[] = dbToAutocomplete(data.customers);
	let designOptions: AutocompleteOption[] = dbToAutocomplete(data.designs);
	let machineOptions: AutocompleteOption[] = dbToAutocomplete(data.machines);
	
</script>

<div class="container h-full mx-auto flex flex-col gap-4 justify-center items-center max-sm:p-4">
	<h2 class="mb-2">Create Order</h2>
	<form class="w-full max-w-lg" method="POST" use:enhance>
		<div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="customer-id"
				>
					Customer
				</label>
				<AutoCompleteSingle form={$form} options={customerOptions} formName="customer_id" reset={resetAutoComplete}/>
			</div>
		</div>

		<div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="design"
				>
					Design
				</label>
				<AutoCompleteSingle form={form} options={designOptions} formName="design_id" reset={resetAutoComplete} />
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="qty">
					Quantity
				</label>
				<input
					required
					class="input"
					id="quantity"
					type="number"
					name="quantity"
					placeholder="Quantity"
					bind:value={$form.quantity}
					{...$constraints.quantity}
				/>
			</div>
		</div>

		<!-- <div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="status"
				>
					Status
				</label>
				<select
					class="select"
					id="status"
					name="status"
					bind:value={$form.status}
					{...$constraints.status}
				>
					<option value="scheduled">Scheduled</option>
					<option value="in_progress">In progress</option>
					<option value="completed">Completed</option>
				</select>
			</div>
		</div> -->
		<!-- <div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="units-produced"
				>
					Units Already Produced
				</label>
				<input
					class="input"
					id="units-produced"
					name="units_already_produced"
					type="number"
					bind:value={$form.units_already_produced}
					{...$constraints.units_already_produced}
				/>
			</div>
		</div> -->
		<div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Specifically Assign Machine
				</label>
				<select
					class="select"
					name="assigned_machine_id"
					size="0"
					bind:value={$form.assigned_machine_id}
					{...$constraints.assigned_machine_id}
				>
					<option value={null}>None - Use Default Machine</option>
					{#each machineOptions as machine}
						<option value={machine.value}>{machine.label}</option>
					{/each}
				</select>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<div class="flex gap-4 align-middle">
					<label
						class="block uppercase tracking-wide text-gray-700 text-xs font-bold"
						for="urgent"
					>
						Urgent
					</label>
					<input
						type="checkbox"
						class="checkbox h-6 w-6"
						id="urgent"
						name="urgent"
						bind:checked={$form.urgent}
						{...$constraints.urgent}
					/>
				</div>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="deadline"
				>
					Deadline
				</label>
				<input
					required
					class="input"
					id="deadline"
					type="date"
					name="deadline"
					bind:value={$form.deadline}
					{...$constraints.deadline}
				/>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-4">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="notes"
				>
					Notes
				</label>
				<textarea
					class="textarea"
					id="notes"
					name="notes"
					bind:value={$form.notes}
					{...$constraints.notes}
				/>
			</div>
		</div>
		{#if Object.keys($errors).length > 0}
			<aside class="alert variant-filled-error p-4" transition:fade|local={{ duration: 500 }}>
				{JSON.stringify($errors)}
			</aside>
		{/if}
		{#if $message}
			<aside
				transition:fade|local={{ duration: 500 }}
				class="alert mb-4"
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
