<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	const { selectedItem, field, title } = $modalStore[0].meta;
	import Icon from '@iconify/svelte';

	export let action: string;
	export let error: string; 

</script>

<div
	class="container h-[50%] w-full max-w-3xl mx-auto flex flex-col gap-4 justify-center items-center bg-surface-200 rounded-lg"
>
	<!-- {#if error}
		<div class="text-red-700 text-xl">{error}</div>
	{/if} -->
	<h2 class="mb-2">Delete {field}</h2>
	<div class="text-lg text-slate-800">
		{title}
	</div>
	<div class="text-xl">Are you sure you want to proceed?</div>
	<form  id="delete-form" class="w-full max-w-lg" method="POST" {action}>
		<slot />
		<input type="hidden" name="id" value={selectedItem.id} />
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
