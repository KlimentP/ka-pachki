<script lang="ts">
	import AutoCompleteMulti from '$lib/components/AutoCompleteMulti.svelte';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import { fade } from 'svelte/transition';
	import { capitalizeString } from '$lib/utils/generic';

	export let form;
	export let data;

	let colorOptions: AutocompleteOption[] = [
		{ value: 'red', label: 'Red' },
		{ value: 'blue', label: 'Blue' },
		{ value: 'green', label: 'Green' },
		{ value: 'yellow', label: 'Yellow' },
		{ value: 'orange', label: 'Orange' },
		{ value: 'purple', label: 'Purple' },
		{ value: 'pink', label: 'Pink' },
		{ value: 'brown', label: 'Brown' },
		{ value: 'black', label: 'Black' },
		{ value: 'white', label: 'White' },
		{ value: 'gray', label: 'Gray' }
	];
	console.log(data)
	let employeeOptions: AutocompleteOption[] = data.employees.map((employee) => {
		return { value: employee.id, label: capitalizeString(employee.name) };}
	)
</script>

<div class="container h-full mx-auto flex flex-col gap-4 justify-center items-center max-sm:p-4">
	<h2 class="mb-2">Create Design</h2>
	{#if form?.error}
		<aside
			transition:fade|local={{ duration: 500 }}
			class="alert variant-filled-error w-full max-w-lg"
		>
			<!-- Message -->
			<div class="alert-message">
				<h3>Error</h3>
				<p>{JSON.stringify(form.error)}</p>
			</div>
		</aside>
	{/if}
	<form class="form w-full max-w-lg" method="POST">
		<!-- <div class="flex flex-wrap -mx-3 mb-6">
		  <div class="w-full px-3">
			<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="design-id">
			  Design ID
			</label>
			<input class="appearance-none block w-full bg-sky-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id="design-id" type="text" placeholder="Design ID">
		  </div>
		</div> -->
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="design-name"
				>
					Design Name
				</label>
				<input class="input" name="name" type="text" placeholder="Design Name" />
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="color-scheme"
				>
					Color Scheme
				</label>
				<AutoCompleteMulti options={colorOptions} formName="color_scheme"/>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Material
				</label>
				<select class="select" name="material" size="4" value="lid">
					<option value="lid">Lid</option>
					<option value="label">Label</option>
					<option value="butter">Butter</option>
					<option value="mebossed_lid">Embossed Lid</option>
				</select>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Preferred Employee
				</label>
				<select class="select" name="preferred_employee" size="4" value="Lid">
					{#each employeeOptions as employee}
						<option value={employee.value}>{employee.label}</option>
					{/each}
				</select>
			</div>
		</div>
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
