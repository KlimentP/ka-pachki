<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	import BaseActionForm from './BaseActionForm.svelte';
	const { selectedOrder} = $modalStore[0].meta;
	export let action: string;
</script>

<BaseActionForm {action}>
	<div class="w-full px-3">
		<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="status">
			Status
		</label>
		<select class="select" id="status" name="status" value={selectedOrder?.status}>
			<option value="scheduled">Scheduled</option>
			<option value="in_progress">In progress</option>
			<option value="completed">Completed</option>
		</select>
	</div>
</BaseActionForm>
