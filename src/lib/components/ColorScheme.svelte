<script lang="ts">
	import { colorMap } from '$lib/utils/colorMap';
	type ObjectKeys<T> = keyof T;
	type colorMapKeys = ObjectKeys<typeof colorMap>;
	export let colors: colorMapKeys[];
</script>

<div class="flex flex-wrap gap-2 py-4">
	{#each colors as color}
		<div
			style="border-color: {colorMap[color]}"
			class="chip chip-hover rounded-xl text-slate-800 border-2 shadow-lg"
		>
			{color}
		</div>
		
	{/each}
</div>
