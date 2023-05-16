<script lang="ts">
	import type { Material } from '$lib/types';
	import TooltipButton from '$lib/components/TooltipButton.svelte';
	import Icon from '@iconify/svelte';
	export let material: Material;
    export let iconHeight = "24";
	export let toolTip = true;

	const materialDict = {
		embossed_lid: 'tabler:texture',
		label: 'quill:label',
		butter: 'fluent-emoji-high-contrast:butter',
		lid: 'openmoji:jar',
		uv_butter: 'tabler:uv-index'
	};
</script>

{#if toolTip}
<div class="w-fit">
<TooltipButton popupText={material}>
	<svelte:fragment slot="button">
		<Icon height={iconHeight} icon={materialDict[material]} />
	</svelte:fragment>
</TooltipButton>
</div>
{:else}
<div class="flex flex-row gap-1 capitalize"> {material} <Icon height={iconHeight} icon={materialDict[material]} /> </div>
{/if}