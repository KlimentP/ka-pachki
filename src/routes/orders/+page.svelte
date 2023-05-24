<script lang="ts">
	import OrderActionItems from '../../lib/components/OrderActionItems.svelte';
	import Icon from '@iconify/svelte';

	import type { PageData } from './$types';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import { dbToAutocomplete } from '$lib/utils/generic';
	import Material from '$lib/components/Material.svelte';
	import ColorScheme from '$lib/components/ColorScheme.svelte';

	export let data: PageData;
	let { tableData, machines } = data;
	// let filter = '';
	// let filteredData = tableData;
	const keysToFilter = [
		'date_created',
		'deadline',
		'status',
		'customer_name',
		'quantity',
		'design_name',
		'material',
		'color_scheme',
		'design_name',
		'machine',
		'urgent',
		'units_already_produced',
		'id'
	];

	function filterObjectByKeys(obj, keys) {
		return keys.reduce((result, key) => {
			if (obj.hasOwnProperty(key)) {
				result[key] = obj[key];
			}
			return result;
		}, {});
	}

	function formatHeaders(header) {
		return header.replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase());
	}
	const filteredData = tableData.map((obj) => filterObjectByKeys(obj, keysToFilter));
	const headers = Object.keys(filteredData[0] || {});
	const machineOptions: AutocompleteOption[] = dbToAutocomplete(machines);

	// function handleFilterChange(event) {
	// 	filter = event.target.value;
	// 	filteredData = tableData.filter((item) =>
	// 		Object.values(item).some((value) =>
	// 			value?.toString().toLowerCase().includes(filter.toLowerCase())
	// 		)
	// 	);
	// }

	// function handleEdit(index) {
	// 	// Add your edit functionality here
	// }

	// function handleDelete(index) {
	// 	tableData.splice(index, 1);
	// 	tableData = [...tableData];
	// }
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center">
	<!-- <input type="text" placeholder="Filter" bind:value={filter} on:input={handleFilterChange} /> -->
	{#if  tableData.length == 0}
	<p>No orders created yet</p>
	{:else}
	<div class="table-container border-primary-400 max-h-[800px] overflow-y-auto">
		<table class="table table-hover text-slate-800 !overflow-x-auto">
			<thead class="rounded-b-none sticky top-0 text-slate-200 !bg-slate-900">
				<tr class="">
					<!-- Add table headers for each field here -->
					<th class="!p-2">Actions</th>
					{#each headers as header}
						{#if header !== 'id' && header !== 'units_already_produced'}
							<th class="!p-2">{formatHeaders(header)}</th>
						{/if}
					{/each}
				</tr>
			</thead>
			<tbody class="rounded-t-none">
				{#each filteredData as item, index}
					<tr class="">
						<td class="">
							<OrderActionItems {machineOptions} {index} {item} />
						</td>
						{#each Object.entries(item) as [key, value]}
							{#if key === 'material'}
								<td class="align-middle"><Material material={value} toolTip={false} /> </td>
							{:else if key === 'color_scheme'}
								<td class="!text-xs"><ColorScheme colors={value} /></td>
							{:else if key === 'urgent'}
								{#if value}
									<td class="flex align-middle text-xs text-rose-700 font-bold"
										><Icon height="32" icon="fluent:alert-urgent-16-regular" /></td
									>
								{:else}
									<td />
								{/if}
							{:else if key === 'quantity'}
								<td>
									{`${item.units_already_produced ?? 0} / ${value} `}
								</td>
							{:else if key === 'date_created'}
							<td>{new Date(value).toISOString().slice(0,10)}</td>
							{:else if key !== 'id' && key !== 'units_already_produced'}
								<td>{value || ''}</td>
							{/if}
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
	{/if}
</div>
