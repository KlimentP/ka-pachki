<script lang="ts">
	import type { PageData } from './$types';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import OrderActionItems from '../../lib/components/OrderActionItems.svelte';
	import { dbToAutocomplete } from '$lib/utils/generic';
	import DataGrid from '$lib/components/DataGrid.svelte';
	import {SelectedOrders} from '$lib/stores/SelectedOrders';
	$: console.log($SelectedOrders)

	export let data: PageData;
	let { tableData, machines, colors } = data;
	const machineOptions: AutocompleteOption[] = dbToAutocomplete(machines);
</script>


<div class="container h-full mx-auto flex flex-col justify-center items-center p-4">
<h2 class="text-2xl font-bold mb-4">Orders</h2>
	<DataGrid {tableData} {machineOptions} {colors} />
</div>
