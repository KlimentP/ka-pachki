<script lang="ts">
	import { Autocomplete } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	export let form: any;
	export let formName: string;
	export let reset = false;
	;
	let input = '';

	// console.log(formName, form)
	// if (!form[formName]) {
	// 	input = '';
	// }
	
	$: if (reset) {
		input = '';
		reset = false;
	}
	export let options: AutocompleteOption[] = [];
	function onSelection(event: any): void {
		input = event.detail.label;
		form[formName] = event.detail.value;
	}
</script>

<input class="input" type="search" bind:value={input} placeholder="Search..." />
<input class="input" name={formName} bind:value={form[formName]} hidden />

<div class="card w-full max-h-48 p-4 overflow-y-auto">
	<Autocomplete bind:input={input} {options} on:selection={onSelection} />
</div>
