<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	const { selectedOrder, field, formType } = $modalStore[0].meta;
	export let action: string;
</script>

<div
	class="container h-[50%] w-full max-w-3xl mx-auto flex flex-col gap-4 justify-center items-center bg-surface-200 rounded-lg"
>
	<h2 class="mb-2">{formType || 'Update'} {field}</h2>
	<div class="text-lg text-slate-800">
		{selectedOrder.customer_name} - {selectedOrder.design_name}
	</div>
	<form class="w-full max-w-lg" method="POST" {action}>
		<slot />
		<input type="hidden" name="id" value={selectedOrder.id} />

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
