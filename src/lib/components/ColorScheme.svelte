<script lang="ts">
	
	export let colorMap: { name: string; code: string }[] = [];
	export let colors: string;
</script>

<div class="flex flex-wrap gap-1 py-2">
	{#each colors as color}
		<div
			style="border-color: {colorMap.find((c) => c?.name === color)?.code}"
			class="chip chip-hover rounded-xl text-xs text-slate-800 border-2 shadow-lg"
		>
			{color}
		</div>
		
	{/each}
</div>
