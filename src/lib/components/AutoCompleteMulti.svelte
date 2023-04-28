<script lang="ts">
	import { Autocomplete, InputChip } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	let inputChip = '';
	
	export let form;
	export let options: AutocompleteOption[] =[];
    export let formName: string;
	export let inputChipList = form[formName];
	function onInputChipSelect(event: any): void {
		if (inputChipList.includes(event.detail.value) === false) {
			inputChipList = [...inputChipList, event.detail.value];
			inputChip = '';
		}
	}
</script>

<InputChip bind:input={inputChip} bind:value={inputChipList} name={formName} data-invalid={form[formName]} />

<div class="card w-full max-h-24 p-4 overflow-y-auto" >
	<Autocomplete
		class="max-h-24"
		bind:input={inputChip}
		{options}
		denylist={inputChipList}
		on:selection={onInputChipSelect}
	/>
</div>
