<script lang="ts">
	import { Autocomplete, InputChip } from '@skeletonlabs/skeleton';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	let inputChip = '';

	export let form: any;
	export let options: AutocompleteOption[] = [];
	export let formName: string;
	export let allowlist: string[] = [];
	export let denylist: string[] = [];
	// export let inputChipList = form[formName];
	function onInputChipSelect(event: any): void {
		if (allowlist.length > 0 && !allowlist.includes(event.detail.value)) {
			console.log('not allowed');
			return;
		}
		form[formName] = [...form[formName], event.detail.value];
		inputChip = '';
	}

</script>

<InputChip
	bind:input={inputChip}
	bind:value={form[formName]}
	name={formName}
	data-invalid={form[formName]}
	validation = {value => {
		if (allowlist.length > 0 && !allowlist.includes(value)) {
			return false;
		}
		return true;
	}}

/>

<div class="card w-full max-h-24 p-4 overflow-y-auto">
	<Autocomplete
		class="max-h-24"
		bind:input={inputChip}
		{options}
		on:selection={onInputChipSelect}
		{allowlist}
		{denylist}
	/>
</div>
