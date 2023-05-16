<script lang="ts">
	import Icon from '@iconify/svelte';
	import { Modal, modalStore, type AutocompleteOption, popup } from '@skeletonlabs/skeleton';
	import type { ModalComponent } from '@skeletonlabs/skeleton';
	import ComboBox from '$lib/components/ComboBox.svelte';
	import TooltipButton from '$lib/components/TooltipButton.svelte';
	import StatusUpdate from '$lib/components/ActionForms/StatusUpdate.svelte';
	import UrgencyUpdate from '$lib/components/ActionForms/UrgencyUpdate.svelte';
	import AssignEmployee from '$lib/components/ActionForms/AssignEmployee.svelte';
	import DeleteItem from '$lib/components/ActionForms/DeleteItem.svelte';
	import UpdateUnitsProduced from '$lib/components/ActionForms/UpdateUnitsProduced.svelte';


	export let item: any;
	export let index: number;
	export let employeeOptions : AutocompleteOption[];
	let selectedOrder = {};

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


</script>

<Modal components={modalComponentRegistry} />

<ComboBox listBoxStyles="" comboboxValue={item.id} closeQuery="">
	<svelte:fragment let:popupCombobox slot="button">
		<button use:popup={popupCombobox}>
			<Icon
				class="text-slate-900 rounded-lg hover:text-primary-500"
				height="24"
				icon="ic:baseline-more-horiz"
			/>
		</button>
	</svelte:fragment>

	<div
		class="flex flex-row gap-2 bg-slate-200 h-24 p-4 rounded-lg border-2
								align-middle mx-auto justify-center items-center shadow-lg"
		slot="listItems"
	>
		<TooltipButton target={`status-hover-${index}`}>
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
				<Icon class="hover:text-primary-500" height="24" icon="carbon:task-complete" />
			</button>
			<div class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48" slot="tooltip">
				Update Status
			</div></TooltipButton
		>
		<TooltipButton target={`urgency-hover-${index}`}>
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
				<Icon class="hover:text-primary-500" height="24" icon="fluent:alert-urgent-16-regular" />
			</button>
			<div class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48" slot="tooltip">
				Change Urgency
			</div>
		</TooltipButton>
		<TooltipButton target={`assign_employee-hover-${index}`}>
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
				<Icon class="hover:text-primary-500" height="24" icon="clarity:assign-user-line" />
			</button>
			<div class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48" slot="tooltip">
				Assign to Specific Employee
			</div>
		</TooltipButton>
		<TooltipButton target={`produced-units-hover-${index}`}>
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
				<Icon class="hover:text-primary-500" height="24" icon="fluent-mdl2:quantity" />
			</button>
			<div class="bg-slate-200 shadow-lg text-slate-800 p-4 text-lg rounded-lg w-48" slot="tooltip">
				Update Produced Units
			</div>
		</TooltipButton>
		<TooltipButton target={`delete-hover-${index}`}>
			<button
				slot="button"
				on:click={() => {
					selectedOrder = item;
					modalStore.trigger({
						type: 'component',
						component: 'modalDeleteItem',
						meta: {
							selectedItem: selectedOrder,
							field: 'Order',
							formType: 'Delete',
							title:
								(selectedOrder?.customer_name || '') + ' - ' + (selectedOrder?.design_name || '')
						}
					});
				}}
			>
				<Icon
					class="hover:text-red-500 "
					height="24"
					icon="material-symbols:delete-outline-sharp"
				/>
			</button>
			<div class="bg-slate-200 shadow-lg text-red-500 p-4 text-lg rounded-lg w-48" slot="tooltip">
				Delete Order
			</div>
		</TooltipButton>
	</div>
</ComboBox>
