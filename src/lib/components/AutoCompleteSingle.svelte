<script lang="ts">
    import { Autocomplete } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';

let input = ''
let actualValue = '';
export let options: AutocompleteOption[] = [];
export let formName: string;
function onSelection(event: any): void {
	input = event.detail.label;
	actualValue = event.detail.value;
}


</script>


<input class="input" type="search" name={formName} bind:value={input} placeholder="Search..." />
<input class="input"  name={formName} bind:value={actualValue}  hidden/>

<div class="card w-full  max-h-48 p-4 overflow-y-auto">
	<Autocomplete bind:input={input} options={options} on:selection={onSelection}  />
</div>