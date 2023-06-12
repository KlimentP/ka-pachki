<script lang="ts">
	import { ListBox, ListBoxItem, type PopupSettings } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';

	export let comboboxValue: string = 'Trigger';
	export let closeQuery = '';
	export let listBoxStyles: string = 'card w-48 shadow-xl py-2 bg-slate-950';
	export let listItems: Array<{ url: string; label: string }> = [];
	let popupCombobox: PopupSettings = {
		event: 'focus-click',
		target: comboboxValue,
		placement: 'bottom',
		closeQuery
	};
</script>

<button class="rounded-2xl" use:popup={popupCombobox}>
	<slot name="button">
		<div class="btn btn-sm variant-ghost-primary text-slate-300 hover:text-primary-500">
			{comboboxValue}
		</div>
	</slot>
</button>
<div class={listBoxStyles} data-popup={comboboxValue}>
	<slot name="listItems">
		<ListBox rounded="rounded-none">
			{#each listItems as item}
				<ListBoxItem
					class="bg-slate-950 "
					bind:group={comboboxValue}
					value={comboboxValue}
					name={item.label}
				>
					<a
						class="flex text-left w-full text-slate-300 hover:text-primary-500 hover:underline-offset-8 hover:underline"
						href={item.url}
					>
						{item.label}
					</a>
				</ListBoxItem>
			{/each}
		</ListBox>
	</slot>
</div>
