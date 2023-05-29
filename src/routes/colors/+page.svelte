<script lang="ts">
	export let data;
	const { colors } = data;
</script>

<div class="flex flex-col gap-8 container h-full mx-auto items-center p-4">
	<div class="text-6xl text-slate-700 underline underline-offset-auto self-center">
		Colors</div>
	<div class="grid grid-cols-8 gap-4">
	{#each colors as color}
		<div class="flex flex-row gap-2">
			<div class="chip chip-hover min-w-[80px] rounded-xl border-2 shadow-lg
			transition-all duration-100 ease-in-out transform hover:scale-105 hover:shadow-xl hover:border-opacity-60"  style="border-color: {color.code}">
			<div>{color.name}</div>
			</div>
		</div>
	{/each}
</div>
</div>
