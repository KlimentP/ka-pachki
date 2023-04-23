<script lang="ts">
	import { ListBox, ListBoxItem, type PopupSettings } from '@skeletonlabs/skeleton';
    import { popup } from '@skeletonlabs/skeleton';

	export let comboboxValue: string;
    export let listItems: Array<{url: string, label: string}>;

	let popupCombobox: PopupSettings = {
		event: 'focus-click',
		target: comboboxValue,
		placement: 'bottom',
		closeQuery: '.listbox-item'
	};
</script>

<button class="btn variant-filled" use:popup={popupCombobox}>
	{comboboxValue ?? 'Trigger'}
</button>
<div class="card w-48 shadow-xl py-2" data-popup={comboboxValue}>
	<ListBox rounded="rounded-none">
        {#each listItems as item}
            <ListBoxItem bind:group={comboboxValue} value={comboboxValue} name={item.label}>
                <a href={item.url}>{item.label}</a>
            </ListBoxItem>
        {/each}
	</ListBox>
	<div class="arrow bg-surface-100-800-token" />
</div>
