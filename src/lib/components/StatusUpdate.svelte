<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';

</script>

<div class="container h-[50%] w-full max-w-3xl mx-auto flex flex-col gap-4 justify-center items-center bg-surface-200 rounded-lg">
	<h2 class="mb-2">Update Status</h2>
	<form class="w-full max-w-lg" method="POST" action="?/updateStatus">
		<div class="w-full px-3">
			<label
				class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
				for="status"
			>
				Status
			</label>
			<select class="select" id="status" name="status">
				<option value="scheduled">Scheduled</option>
				<option value="in_progress">In progress</option>
				<option value="completed">Completed</option>
			</select>
		</div>
        <input type="hidden" name="order_id" value={$modalStore[0].meta.selectedOrderId} />
        <div class="w-full p-3">
            <button
                class="bg-primary-500 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                type="submit"
            >
                Submit
            </button>
        </div>
	</form>
</div>
