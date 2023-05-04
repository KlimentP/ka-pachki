<script lang="ts">
	import type { Database } from '../../supabase';
	import { capitalizeString } from '$lib/utils/generic';
	export let items: any;
	// Database['public']['Tables']['designs']['Row'][] = [];

// 	const colorVariants = {
// 		blue: 'chip text-slate-800  border border-4 rounded-xl border-blue-500  hover:bg-blue-500',
// 		red: 'chip text-slate-800  border border-4 rounded-xl border-red-500 hover:bg-red-500',
// 		green: 'chip text-slate-800  border border-4 rounded-xl border-green-500 hover:bg-green-500',
// 		yellow: 'chip text-slate-800  border border-4 rounded-xl border-yellow-500 hover:bg-yellow-500',
// 		default: 'chip text-slate-800  border border-4 rounded-xl border-gray-500 hover:bg-gray-500'
// 	};
// </script>

<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-16 p-16 overflow-y-auto max-h-screen">
	{#each items as item (item.name)}
		<div class="card card-hover rounded-xl shadow-lg">
			<header class="card-header bg-slate-800  rounded-t-lg shadow-lg p-4 
      text-lg font-bold mb-2 text-slate-300 hover:text-primary-500" >
					{capitalizeString(item.name)}
			</header>
			<section class="p-4">
				<div class="flex flex-wrap gap-2 py-4">
					{#each item.color_scheme as color}
						<div
							style="border-color: {color}"
							class="chip chip-hover rounded-xl text-slate-800 border-2 shadow-lg"
						>
							{color}
						</div>
					{/each}
				</div>
				<div class="text-xl text-slate-800">Material: {capitalizeString(item.material)}</div>
			</section>
			{#if item?.employees?.name}
			<div class="card-footer">
				<div class="text-lg text-slate-800 border ">
					Preferred Employee: {item?.employees?.name || 'None'}
				</div>
			</div>
			{/if}
		</div>
	{/each}
</div>
