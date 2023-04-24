<script lang="ts">
    import { Autocomplete } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';

let input = ''
export let options: AutocompleteOption[] = [];
function onSelection(event: any): void {
	input = event.detail.label;
}


</script>


<input class="input" type="search" name="demo" bind:value={input} placeholder="Search..." />
<div class="card w-full  max-h-48 p-4 overflow-y-auto">
	<Autocomplete bind:input={input} options={options} on:selection={onSelection} />
</div>