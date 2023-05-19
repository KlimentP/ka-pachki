<script lang="ts">
	export let title: string = '(Title)';
	export let timestamp: string = '';
	export let description: string = '(Description)';
	export let badgeText: string = '';
	// export let height: string = 'auto';
	// const heightString = height === 'auto' ? 'height: auto;' : ` height: ${height}px;`;

</script>

<li class="flex flex-col gap-2 ml-10">
	<!-- Slot: Icon -->
	<span
		class="absolute flex items-center justify-center w-6 h-6 bg-secondary-300 text-secondary-900 font-bold rounded-full -left-3 ring-8 ring-surface-200-700-token"
	>
		<slot name="icon">&hearts;</slot>
	</span>
	<!-- Title -->
	<h3 class="flex items-center gap-2 space-x-2 -translate-y-2 capitalize">
		<span>{title}</span>
		<!-- Badge -->
		{#if badgeText}
			<span class="badge variant-soft-surface self-start">{badgeText}</span>
		{/if}
	</h3>
	<!-- Timestamp -->
	{#if timestamp}
		<time class="block">Due on {timestamp}</time>
	{/if}
	<!-- Description -->
	<!-- <p class="opacity-75">{description}</p> -->
	<!-- Slot: Default -->
	{#if $$slots.default}<div><slot /></div>{/if}
</li>
