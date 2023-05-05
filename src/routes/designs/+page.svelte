
<script lang="ts">
	import { Toast, toastStore } from '@skeletonlabs/skeleton';

	import DesignsList from '$lib/components/DesignsList.svelte';

	export let data;
	export let form;
	let {tableData} = data;
	if (form?.error) {
		console.log('triggering toast')
		toastStore.trigger({
					message: `Error: ${form.error}`,
					background: 'bg-red-500',
		});
	} else if (form?.message) {
		toastStore.trigger({
					message: `Success: ${form.message}`,
					background: 'bg-green-500',
		});
	}

	</script>
<Toast/>
<div class="container h-full mx-auto flex justify-center items-center">
	<DesignsList items={tableData} />
</div>
