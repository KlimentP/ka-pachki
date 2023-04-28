<script lang="ts">
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	export let form;
	export let formName: string;
	let actualValue = form[formName];
	let input = '';
	export let options: AutocompleteOption[] = [];
	function onSelection(event: any): void {
		input = event.detail.label;
		actualValue = event.detail.value;
	}
</script>

<input class="input" type="search" bind:value={input} placeholder="Search..." />
<input class="input" name={formName} bind:value={actualValue} hidden />

<div class="card w-full max-h-48 p-4 overflow-y-auto">
	<Autocomplete bind:input {options} on:selection={onSelection} />
</div>
