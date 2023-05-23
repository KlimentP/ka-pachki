<script lang="ts">

	import Material from '$lib/components/Material.svelte';
	import ColorScheme from '$lib/components/ColorScheme.svelte';
	export let item: any;
	</script>

		<div class="p-4 flex flex-col gap-2 justify-start">
			<section class="">
				<ColorScheme colors={item.color_scheme} />
				<div class="flex flex-row flex-wrap gap-2 ">
					<div class="text-slate-800 font-bold">Material:</div>
					<div class=""><Material iconHeight="24" material={item.material} /></div>
					{#if item?.machines?.name}
						<div class="font-bold text-slate-800">Preferred Machine:</div>
						<span class="text-slate-800">{item?.machines?.name || 'None'}</span>
					{/if}
				</div>
			</section>
		</div>

