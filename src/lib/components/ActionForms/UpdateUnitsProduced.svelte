<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	import BaseActionForm from './BaseActionForm.svelte';
	const { selectedOrder } = $modalStore[0].meta;
	export let action: string;
</script>

<BaseActionForm {action}>
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
            value={selectedOrder?.units_already_produced}
		/>
	</div>
</BaseActionForm>
