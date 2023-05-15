<script lang="ts">
	import { Modal, modalStore } from '@skeletonlabs/skeleton';
	import type { ModalComponent } from '@skeletonlabs/skeleton';
	import DeleteItem from '$lib/components/ActionForms/DeleteItem.svelte';
	import { capitalizeString } from '$lib/utils/generic';
	import Icon from '@iconify/svelte';
	import { Toast, toastStore } from '@skeletonlabs/skeleton';

	export let items: any;
	export let form;
	export let itemType: string;

	const itemCapitalized = capitalizeString(itemType);
	const itemPlural = `${itemCapitalized}s`;
	let searchTerm = '';
	let fiteredItems = items;
	$: if (searchTerm) {
		fiteredItems = items.filter((item: any) => {
			return item.name.toLowerCase().includes(searchTerm.toLowerCase());
		});
	} else {
		fiteredItems = items;
	}
	let selectedItem: {};

	const modalComponentRegistry: Record<string, ModalComponent> = {
		modalDeleteItem: { ref: DeleteItem, props: { action: `?/delete${itemCapitalized}` } }
	};

	if (form?.error) {
		console.log('error');

		toastStore.trigger({
			message: `Error: ${form.error}`,
			background: 'bg-red-500'
		});
	} else if (form?.message) {
		console.log('deleted');
		toastStore.trigger({
			message: `Success: ${form.message}`,
			background: 'bg-green-500'
		});
	}
</script>

<Modal components={modalComponentRegistry} />
<Toast />

<div class="flex flex-col py-8 px-2 gap-8">
	<div class="text-6xl text-slate-700 underline underline-offset-auto self-center">
		{itemPlural}
	</div>
	<div>
		<label
			for="search-name"
			class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
			>Search {itemPlural}</label
		>
		<input
			class="input w-64"
			name="search-name"
			type="text"
			placeholder={`${itemCapitalized} Name`}
			bind:value={searchTerm}
		/>
	</div>
	{#if fiteredItems.length === 0}
		<p>No {itemPlural} Found</p>
	{:else}
		<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-16 overflow-y-auto max-h-[560px] overflow-x-hidden">
			{#each fiteredItems as item (item.name)}
				<div class="card card-hover rounded-xl shadow-lg">
					<header
						class="flex flex-row card-header bg-slate-800 rounded-t-lg shadow-lg p-4 text-lg font-bold text-slate-300 hover:text-primary-500"
					>
						<div>
							{capitalizeString(item.name)}
						</div>
						<button
							class="self-center ml-auto"
							on:click={() => {
								selectedItem = item;
								modalStore.trigger({
									type: 'component',
									component: 'modalDeleteItem',
									meta: {
										selectedItem: selectedItem,
										field: itemCapitalized,
										title: item.name || ''
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
					</header>
					<slot name="item-body" {item} />
				</div>
			{/each}
		</div>
	{/if}
</div>
