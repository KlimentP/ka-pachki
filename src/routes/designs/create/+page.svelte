<script lang="ts">

	import AutoCompleteMulti from "$lib/components/AutoCompleteMulti.svelte";
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';

	let colorOptions: AutocompleteOption[] = [
		{ value: 'red', label: 'Red' },
		{ value: 'blue', label: 'Blue' },
		{ value: 'green', label: 'Green' },
		{ value: 'yellow', label: 'Yellow' },
		{ value: 'orange', label: 'Orange' },
		{ value: 'purple', label: 'Purple' },
		{ value: 'pink', label: 'Pink' },
		{ value: 'brown', label: 'Brown' },
		{ value: 'black', label: 'Black' },
		{ value: 'white', label: 'White' },
		{ value: 'gray', label: 'Gray' },
	];

</script>
<div class="container h-full mx-auto flex flex-col justify-center items-center max-sm:p-4">
	<h2 class="mb-2">Create Design</h2>
	<form class="w-full max-w-lg">
		<!-- <div class="flex flex-wrap -mx-3 mb-6">
		  <div class="w-full px-3">
			<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="design-id">
			  Design ID
			</label>
			<input class="appearance-none block w-full bg-sky-100 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id="design-id" type="text" placeholder="Design ID">
		  </div>
		</div> -->
		<div class="flex flex-wrap -mx-3 mb-6">
		  <div class="w-full px-3">
			<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="design-name">
			  Design Name
			</label>
			<input class="input" id="design-name" type="text" placeholder="Design Name">
		  </div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
		  <div class="w-full px-3">
			<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="color-scheme">
			  Color Scheme
			</label>
			<AutoCompleteMulti options={colorOptions} />
		  </div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
			  <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="material">
				Material
			  </label>
			  <select class="select" id="material" size="4" value="Lid">
				<option value="Lid">Lid</option>
				<option value="Label">Label</option>
				<option value="Butter">Butter</option>
				<option value="Embossed Lid">Embossed Lid</option>
			  </select>
			</div>
		  </div>
		<div class="flex flex-wrap -mx-3 mb-2">
		  <div class="w-full px-3">
			<button class="bg-primary-500 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
			  Submit
			</button>
		  </div>
		</div>
	  </form>
	  
</div>
