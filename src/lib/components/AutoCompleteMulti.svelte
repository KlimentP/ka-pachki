<script lang="ts">
	import { Autocomplete, InputChip } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	let inputChip = '';
	
	let inputChipList: string[] = [];
	
	export let options: AutocompleteOption[] =[];
    export let formName: string;
	function onInputChipSelect(event: any): void {
		if (inputChipList.includes(event.detail.value) === false) {
			inputChipList = [...inputChipList, event.detail.value];
			inputChip = '';
		}
	}
</script>

<InputChip bind:input={inputChip} bind:value={inputChipList} name={formName} />

<div class="card w-full max-h-48 p-4 overflow-y-auto" >
	<Autocomplete
		bind:input={inputChip}
		{options}
		denylist={inputChipList}
		on:selection={onInputChipSelect}
	/>
</div>
