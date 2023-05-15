<script lang="ts">
	export let item: any;
	const statusFill = {
		in_progress: 'badge variant-filled bg-primary-500',
		scheduled: 'badge variant-filled bg-surface-500',
		completed: 'badge variant-filled bg-green-500'
	};
</script>

<div class="w-ful h-64 overflow-y-auto p-4">
	<dl class="list-dl">
		{#each item?.orders as order}
			{#if order}
				<div class="!rounded-lg flex flex-wrap " class:bg-amber-300="{order.urgent}">
					<dt class="font-bold">{order?.designs?.name}</dt>
					<dd class="text-sm opacity-50">{order?.quantity}</dd>
					<dd class={statusFill[order?.status]}>{order?.status}</dd>
					<dd class="badge">{order?.deadline ?? 'unknown'}</dd>

				</div>
				<hr />
			{/if}
		{/each}
	</dl>
</div>
