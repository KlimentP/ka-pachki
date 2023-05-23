<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	import BaseActionForm from './BaseActionForm.svelte';
	const { selectedOrder, machineOptions } = $modalStore[0].meta;
	export let action: string;
</script>

<BaseActionForm {action}>
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
			size="4"
			bind:value={selectedOrder.assigned_machine_id}
		>
			{#each machineOptions as machine}
				<option value={machine.value}>{machine.label}</option>
			{/each}
		</select>
	</div>
</BaseActionForm>
