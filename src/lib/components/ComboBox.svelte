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
		closeQuery,

	};
</script>

<button
	class="btn variant-ghost-primary text-slate-300 hover:text-primary-500"
	use:popup={popupCombobox}
>
	<slot name="button">
		{comboboxValue}
	</slot>
</button>
<div class={listBoxStyles} data-popup={comboboxValue}>
	<slot name="listItems">
		<ListBox rounded="rounded-none">
			{#each listItems as item}
				<a href={item.url}>
					<ListBoxItem
						class="bg-slate-950 text-slate-300 hover:text-primary-500"
						bind:group={comboboxValue}
						value={comboboxValue}
						name={item.label}
					>
						{item.label}
					</ListBoxItem>
				</a>
			{/each}
		</ListBox>
	</slot>
</div>
