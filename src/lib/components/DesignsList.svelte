<script lang="ts">
	import type { Database } from '../../supabase';
	import { capitalizeString } from '$lib/utils/generic';
	export let items: Database['public']['Tables']['designs']['Row'][] = [];

	const colorVariants = {
		blue: 'chip text-slate-800  border border-4 rounded-xl border-blue-500  hover:bg-blue-500',
		red: 'chip text-slate-800  border border-4 rounded-xl border-red-500 hover:bg-red-500',
		green: 'chip text-slate-800  border border-4 rounded-xl border-green-500 hover:bg-green-500',
		yellow: 'chip text-slate-800  border border-4 rounded-xl border-yellow-500 hover:bg-yellow-500',
		default: 'chip text-slate-800  border border-4 rounded-xl border-gray-500 hover:bg-gray-500'
	};
</script>

<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
	{#each items as item (item.name)}
		<div class="card card-hover rounded-xl shadow-lg">
			<header class="card-header bg-primary-600 rounded-t-lg shadow-lg p-4">
				<h3 class="text-lg font-bold mb-2 text-slate-300">
					{capitalizeString(item.name)}
				</h3>
			</header>
			<section class="p-4">
				<div class="flex flex-wrap gap-2 py-4">
					{#each item.color_scheme as color}
						<div
							class={colorVariants.hasOwnProperty(color) // @ts-ignore
								? colorVariants[color] 
								: colorVariants.default}
						>
							{color}
						</div>
					{/each}
				</div>
				<div class="text-xl text-slate-800">Material: {capitalizeString(item.material)}</div>
			</section>
			<div class="card-footer">
				<div class="text-lg text-slate-800">
					Preferred Employee: {item.preferred_employee || 'None'}
				</div>
			</div>
		</div>
	{/each}
</div>
