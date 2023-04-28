<script lang="ts">
	import AutoCompleteSingle from '$lib/components/AutoCompleteSingle.svelte';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import { dbToAutocomplete, capitalizeString } from '$lib/utils/generic';
	import { fade } from 'svelte/transition';
	import { superForm } from 'sveltekit-superforms/client';
	import { page } from '$app/stores';
	export let data;

	let customerOptions: AutocompleteOption[] = dbToAutocomplete(data.customers);
	let designOptions: AutocompleteOption[] = dbToAutocomplete(data.designs);
	let employeeOptions: AutocompleteOption[] = dbToAutocomplete(data.employees);
	const { form, errors, constraints, enhance, delayed, message, empty } = superForm(data.form);
	console.log(designOptions);
</script>

<div class="container h-full mx-auto flex flex-col gap-4 justify-center items-center max-sm:p-4">
	<h2 class="mb-2">Create Order</h2>
	<form class="w-full max-w-lg" method="POST">
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="customer-id"
				>
					Customer
				</label>
				<AutoCompleteSingle form={$form} options={customerOptions} formName="customer_id" />
			</div>
		</div>

		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="design"
				>
					Design
				</label>
				<AutoCompleteSingle form={$form}  options={designOptions} formName="design_id" />
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
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

		<div class="flex flex-wrap -mx-3 mb-6">
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
					bind:value={$form.status }
					{...$constraints.status}
				>
					<option value="scheduled">Scheduled</option>
					<option value="in_progress">In progress</option>
					<option value="completed">Completed</option>
				</select>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
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
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Specifically Assign Employee
				</label>
				<select
					class="select"
					name="assigned_employee_id"
					size="4"
					bind:value={$form.assigned_employee_id}
					{...$constraints.assigned_employee_id}
				>
					{#each employeeOptions as employee}
						<option value={employee.value}>{employee.label}</option>
					{/each}
				</select>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<div class="relative">
					<label
						class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
						for="urgent"
					>
						Urgent
					</label>
					<select class="select" id="urgent" name="urgent" bind:value={$form.urgent} {...$constraints.urgent}>
						<option value="false">No</option>
						<option value="true">Yes</option>
					</select>
					<div
						class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
					>
						<svg
							class="fill-current h-4 w-4"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
						>
							<path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
							<path
								fill-rule="evenodd"
								d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12z"
							/>
						</svg>
					</div>
				</div>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="deadline"
				>
					Deadline
				</label>
				<input
					class="input"
					id="deadline"
					type="date"
					name="deadline"
					bind:value={$form.deadline}
					{...$constraints.deadline}
				/>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="notes"
				>
					Notes
				</label>
				<textarea class="textarea" id="notes" name="notes" bind:value={$form.notes} {...$constraints.notes} />
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
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
		</div>
	</form>
</div>
