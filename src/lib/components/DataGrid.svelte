<script lang="ts">
	import { readable } from 'svelte/store';
	import { SelectedOrders } from '$lib/stores/SelectedOrders';
	import Icon from '@iconify/svelte';
	import SelectIndicator from '$lib/components/SelectIndicator.svelte';

	import { createTable, Subscribe, Render, createRender } from 'svelte-headless-table';
	import {
		addColumnFilters,
		addColumnOrder,
		addHiddenColumns,
		addSortBy,
		addTableFilter,
		addPagination,
		addExpandedRows,
		matchFilter,
		numberRangeFilter,
		textPrefixFilter,
		addSubRows,
		addGroupBy,
		addSelectedRows,
		addResizedColumns
	} from 'svelte-headless-table/plugins';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import OrderActionItems from './OrderActionItems.svelte';
	import { dbToAutocomplete } from '$lib/utils/generic';
	import Material from '$lib/components/Material.svelte';
	import ColorScheme from '$lib/components/ColorScheme.svelte';

	export let tableData: any[];
	export let height = '800px';

	export let machineOptions: AutocompleteOption[];
	export let colors: any;
	const tableInput = readable(tableData);
	const table = createTable(tableInput, {
		hide: addHiddenColumns({ initialHiddenColumnIds: ['id'] }),
		sort: addSortBy({
			initialSortKeys: [
				{
					id: 'date_created',
					order: 'asc'
				}
			]
		}),
		select: addSelectedRows(),
		orderColumns: addColumnOrder({
			initialColumnIdOrder: [
				'selected',
				'actions',
				'urgent',
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
				'id'
			]
		})
	});

	const genericCols = [
		// 'date_created',
		'deadline',
		'status',
		'customer_name',
		// 'quantity',
		'design_name',
		// 'material',
		// 'color_scheme',
		'machine',
		// 'urgent',
		// 'units_already_produced',
		'id'
	];

	function formatHeaders(header: string) {
		return header.replaceAll('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase());
	}

	let colDefs: any[] = genericCols.map((col) =>
		table.column({
			accessor: col,
			header: formatHeaders(col),
			cell: ({ value }) => value ?? ''
		})
	);
	colDefs = [
		table.display({
			id: 'selected',
			header: '',
			cell: ({ row }, { pluginStates }) => {
				const { isSelected, isSomeSubRowsSelected } = pluginStates.select.getRowState(row);
				return createRender(SelectIndicator, {
					isSelected,
					isSomeSubRowsSelected
				});
			}
		}),
		table.display({
			id: 'actions',
			accessor: 'actions',
			header: 'Actions',
			cell: ({ row }) =>
				createRender(OrderActionItems, { item: row.original, index: row.id, machineOptions })
		}),
		table.column({
			accessor: 'material',
			header: 'Material',
			cell: ({ row }) => createRender(Material, { material: row.original.material })
		}),
		table.column({
			accessor: 'color_scheme',
			header: 'Color Scheme',
			cell: ({ row }) =>
				createRender(ColorScheme, { colors: row.original.color_scheme, colorMap: colors })
		}),
		table.column({
			accessor: 'urgent',
			header: 'Urgent',
			cell: ({ row }) =>
				row.original.urgent
					? createRender(Icon, {
							height: '32',
							icon: 'fluent:alert-urgent-16-regular',
							color: 'red'
					  })
					: ''
		}),
		table.column({
			accessor: 'quantity',
			header: 'Quantity',
			cell: ({ row }) => `${row.original.units_already_produced ?? 0} / ${row.original.quantity} `
		}),
		table.column({
			accessor: 'date_created',
			header: 'Date Created',
			cell: ({ value }) => new Date(value).toISOString().slice(0, 10)
		}),
		...colDefs
	];

	const columns = table.createColumns(colDefs);

	const { headerRows, rows, tableAttrs, tableBodyAttrs, pluginStates } =
		table.createViewModel(columns);
	const { selectedDataIds, allRowsSelected } = pluginStates.select;
	const handleSelectAll = (event: any) => {
		if (event.target.checked) {
			allRowsSelected.set(true);
		} else {
			selectedDataIds.set({});
		}
	};

	$: SelectedOrders.set(
		tableData.filter((_: any, index: number) =>
			Object.keys($selectedDataIds).includes(index.toString())
		)
	);
</script>

<!-- <input type="text" placeholder="Filter" bind:value={filter} on:input={handleFilterChange} /> -->
<div>
	{#if tableData.length == 0}
		<p>No orders created yet</p>
	{:else}
		<div class="table-container overflow-y-auto" style={`max-height: ${height} `}>
			<table class="table table-hover text-slate-800 !overflow-x-auto" {...$tableAttrs}>
				<thead class="rounded-b-none sticky top-0 text-slate-200 !bg-slate-900">
					{#each $headerRows as headerRow (headerRow.id)}
						<Subscribe rowAttrs={headerRow.attrs()} let:rowAttrs>
							<tr {...rowAttrs}>
								{#each headerRow.cells as cell (cell.id)}
									<Subscribe attrs={cell.attrs()} let:attrs props={cell.props()} let:props>
										<th
											on:click={props.sort.toggle}
											class:sorted={props.sort.order !== undefined}
											{...attrs}
										>
											<div class="flex gap-1 align-middle justify-center">

												{#if cell.id !== 'selected' && cell.id !== 'actions' && cell.id !== 'urgent'}
												<div class="self-center">
													<Render of={cell.render()} />
												</div>
													{#if props.sort.order === 'asc'}
														<div class="text-2xl text-primary-500">↓</div>
													{:else if props.sort.order === 'desc'}
														<div class="text-2xl text-primary-500">↑</div>
													{:else if props.sort.order === undefined}
														<div class="text-2xl">↓↑</div>
													{/if}
												{:else if cell.id === 'selected'}
													<div class="self-start">
														<input
															class="checkbox h-6 w-6"
															type="checkbox"
															on:change={handleSelectAll}
														/>
													</div>
												{/if}

											</div>
										</th>
									</Subscribe>
								{/each}
							</tr>
						</Subscribe>
					{/each}
				</thead>
				<tbody {...$tableBodyAttrs}>
					{#each $rows as row (row.id)}
						<Subscribe rowAttrs={row.attrs()} let:rowAttrs rowProps={row.props()} let:rowProps>
							<tr {...rowAttrs} class:!bg-slate-400={rowProps.select.selected}>
								{#each row.cells as cell (cell.id)}
									<Subscribe attrs={cell.attrs()} let:attrs>
										<td {...attrs}>
											<Render of={cell.render()} />
										</td>
									</Subscribe>
								{/each}
							</tr>
						</Subscribe>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
