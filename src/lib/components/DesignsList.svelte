<script lang="ts">
  import ColorScheme from '$lib/components/ColorScheme.svelte';

	import { Modal, modalStore } from '@skeletonlabs/skeleton';
	import type { ModalComponent } from '@skeletonlabs/skeleton';
	import DeleteItem from '$lib/components/ActionForms/DeleteItem.svelte';

	import { capitalizeString } from '$lib/utils/generic';
	import { colorMap } from '$lib/utils/colorMap';

	import Icon from '@iconify/svelte';
	export let items: any;
	let searchTerm = '';
	let fiteredItems = items;

	$: if (searchTerm) {
		fiteredItems = items.filter((item: any) => {
			return item.name.toLowerCase().includes(searchTerm.toLowerCase());
		});
	} else {
		fiteredItems = items;
	}
	let selectedDesign: {};

	const modalComponentRegistry: Record<string, ModalComponent> = {
		modalDeleteItem: { ref: DeleteItem, props: { action: '?/deleteDesign' } }
	};
</script>

<Modal components={modalComponentRegistry} />
<div class="flex flex-col py-8 px-2 gap-8">
	<div>
		<label
			for="search-name"
			class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
			>Search Designs</label
		>
		<input
			class="input w-64"
			name="search-name"
			type="text"
			placeholder="Design Name"
			bind:value={searchTerm}
		/>
	</div>
	{#if fiteredItems.length === 0}
		<p>No Designs Found</p>
	{:else}
		<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-16 overflow-y-auto max-h-screen">
			{#each fiteredItems as item (item.name)}
				<div class="card card-hover rounded-xl shadow-lg">
					<header
						class="card-header bg-slate-800 rounded-t-lg shadow-lg p-4 text-lg font-bold mb-2 text-slate-300 hover:text-primary-500"
					>
						{capitalizeString(item.name)}
					</header>
					<div class="p-4 flex flex-col gap-2 justify-start">
						<section class="">
							<ColorScheme colors={item.color_scheme}/>
							<div class="text-xl text-slate-800">Material: {capitalizeString(item.material)}</div>
						</section>
						{#if item?.employees?.name}
							<div class="text-lg text-slate-800">
								Preferred Employee: {item?.employees?.name || 'None'}
							</div>
						{/if}
						<button
							on:click={() => {
								selectedDesign = item;
								modalStore.trigger({
									type: 'component',
									component: 'modalDeleteItem',
									meta: { selectedItem: selectedDesign, field: 'Design', title: item.name || '' }
								});
							}}
						>
							<Icon
								class="hover:text-red-500 "
								height="24"
								icon="material-symbols:delete-outline-sharp"
							/>
						</button>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
