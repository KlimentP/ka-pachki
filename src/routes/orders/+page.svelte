<script lang="ts">
	import Icon from '@iconify/svelte';
	import type { PageData } from './$types';
	import { Modal, modalStore, type AutocompleteOption } from '@skeletonlabs/skeleton';
	import type { ModalComponent } from '@skeletonlabs/skeleton';
	import ComboBox from '$lib/components/ComboBox.svelte';
	import TooltipButton from '$lib/components/TooltipButton.svelte';
	import StatusUpdate from '$lib/components/ActionForms/StatusUpdate.svelte';
	import UrgencyUpdate from '$lib/components/ActionForms/UrgencyUpdate.svelte';
	import AssignEmployee from '$lib/components/ActionForms/AssignEmployee.svelte';
	import DeleteItem from '$lib/components/ActionForms/DeleteItem.svelte';
	import UpdateUnitsProduced from '$lib/components/ActionForms/UpdateUnitsProduced.svelte';
	import { dbToAutocomplete } from '$lib/utils/generic';

	export let data: PageData;
	let { tableData, employees } = data;
	let selectedOrder = {};
	// let filter = '';
	// let filteredData = tableData;
	const keysToFilter = [
		'date_created',
		'status',
		'customer_name',
		'quantity',
		'design_name',
		'material',
		'color_scheme',
		'deadline',
		'design_name',
		'employee',
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

	const modalComponentRegistry: Record<string, ModalComponent> = {
		modalStatusUpdate: { ref: StatusUpdate, props: { action: '?/updateStatus' } },
		modalUrgencyUpdate: { ref: UrgencyUpdate, props: { action: '?/updateUrgency' } },
		modalAssignEmployee: { ref: AssignEmployee, props: { action: '?/assignEmployee' } },
		modalUpdateUnitsProduced: {
			ref: UpdateUnitsProduced,
			props: { action: '?/updateUnitsProduced' }
		},
		modalDeleteItem: { ref: DeleteItem, props: { action: '?/deleteOrder' } }
	};

	const filteredData = tableData.map((obj) => filterObjectByKeys(obj, keysToFilter));
	const headers = Object.keys(filteredData[0] || {});
	const employeeOptions: AutocompleteOption[] = dbToAutocomplete(employees);

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

<Modal components={modalComponentRegistry} />
<div class="container h-full mx-auto flex flex-col gap-4 justify-center items-center">
	<!-- <input type="text" placeholder="Filter" bind:value={filter} on:input={handleFilterChange} /> -->
	<div class="table-container border-primary-400 overflow-auto">
		<table class="table table-comfortable table-auto bg-primary-200 text-slate-800">
			<thead class="text-primary-400 !bg-slate-900">
				<tr>
					<!-- Add table headers for each field here -->
					<th>Actions</th>
					{#each headers as header}
						<th>{header}</th>
					{/each}
				</tr>
			</thead>
			<tbody>
				{#each filteredData as item, index}
					<tr>
						<td class="">
							<ComboBox listBoxStyles="" comboboxValue={item.id} closeQuery="">
								<Icon
									class="text-slate-900"
									slot="button"
									height="24"
									icon="ic:baseline-more-horiz"
								/>
								<div
									class="flex flex-row gap-2 bg-slate-200 h-24 p-4 rounded-lg border-2
								align-middle mx-auto justify-center items-center shadow-lg"
									slot="listItems"
								>
									<TooltipButton target="status-hover">
										<button
											type="button"
											slot="button"
											on:click={() => {
												selectedOrder = item;

												modalStore.trigger({
													type: 'component',
													component: 'modalStatusUpdate',
													meta: { selectedOrder, field: 'Status' }
												});
											}}
											class=""
										>
											<Icon
												class="hover:text-primary-500"
												height="24"
												icon="carbon:task-complete"
											/>
										</button>
										<div
											class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48"
											slot="tooltip"
										>
											Update Status
										</div></TooltipButton
									>
									<TooltipButton target="status-urgency">
										<button
											slot="button"
											on:click={() => {
												selectedOrder = item;

												modalStore.trigger({
													type: 'component',
													component: 'modalUrgencyUpdate',
													meta: { selectedOrder, field: 'Urgent Status' }
												});
											}}
											class=""
										>
											<Icon
												class="hover:text-primary-500"
												height="24"
												icon="fluent:alert-urgent-16-regular"
											/>
										</button>
										<div
											class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48"
											slot="tooltip"
										>
											Change Urgency
										</div>
									</TooltipButton>
									<TooltipButton target="assign-employee-hover">
										<button
											slot="button"
											on:click={() => {
												selectedOrder = item;

												modalStore.trigger({
													type: 'component',
													component: 'modalAssignEmployee',
													meta: { selectedOrder, field: 'Employee Assignment', employeeOptions }
												});
											}}
										>
											<Icon
												class="hover:text-primary-500"
												height="24"
												icon="clarity:assign-user-line"
											/>
										</button>
										<div
											class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48"
											slot="tooltip"
										>
											Assign to Specific Employee
										</div>
									</TooltipButton>
									<TooltipButton target="produced-units-hover">
										<button
											slot="button"
											on:click={() => {
												selectedOrder = item;
												modalStore.trigger({
													type: 'component',
													component: 'modalUpdateUnitsProduced',
													meta: { selectedOrder, field: 'Units Produced' }
												});
											}}
										>
											<Icon
												class="hover:text-primary-500"
												height="24"
												icon="fluent-mdl2:quantity"
											/>
										</button>
										<div
											class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48"
											slot="tooltip"
										>
											Update Produced Units
										</div>
									</TooltipButton>
									<TooltipButton target="delete-hover">
										<button
											slot="button"
											on:click={() => {
												selectedOrder = item;
												modalStore.trigger({
													type: 'component',
													component: 'modalDeleteItem',
													meta: { selectedItem: selectedOrder, field: 'Order', formType: 'Delete', 
												title: (selectedOrder?.customer_name || '') + ' - ' + (selectedOrder?.design_name || '') }
												});
											}}
										>
											<Icon
												class="hover:text-red-500 "
												height="24"
												icon="material-symbols:delete-outline-sharp"
											/>
										</button>
										<div
											class="bg-slate-200 shadow-lg text-red-500 p-4 text-lg rounded-lg w-48"
											slot="tooltip"
										>
											Delete Order
										</div>
									</TooltipButton>
								</div>
							</ComboBox>
						</td>
						{#each Object.values(item) as value}
							<td>{value || ''}</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
