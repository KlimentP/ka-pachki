<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	const { selectedOrder, field, formType } = $modalStore[0].meta;
	import Icon from '@iconify/svelte';

	export let action: string;
</script>

<div
	class="container h-[50%] w-full max-w-3xl mx-auto flex flex-col gap-4 justify-center items-center bg-surface-200 rounded-lg"
>
	<h2 class="mb-2">{formType || 'Update'} {field}</h2>
	<div class="text-lg text-slate-800">
		{selectedOrder.customer_name || ''} - {selectedOrder.design_name}
	</div>
	<div class="text-xl">Are you sure you want to proceed?</div>
	<form id="delete-form" class="w-full max-w-lg" method="POST" {action}>
		<slot />
		<input type="hidden" name="order_id" value={selectedOrder.order_id} />
	</form>
	<div class="flex flex-row gap-2 justify-center">
		<div>
			<button
				class="bg-red-700 hover:bg-red-900 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
				type="submit"
                form="delete-form"
			>
				Delete
			</button>
		</div>
		<div>
			<button
				class="button text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline bg-slate-700 hover:bg-slate-900"
				type="submit"
				on:click={() => modalStore.close()}
			>
				<Icon height="24" icon="ic:sharp-close" />
			</button>
		</div>
	</div>
</div>
