<script lang="ts">
	import Timeline from '$lib/components/Timeline/Timeline.svelte';
	import TimelineItem from '$lib/components/Timeline/TimelineItem.svelte';
	import Icon from '@iconify/svelte';
	import { convertMinutesToHoursMinutes, dbToAutocomplete } from '$lib/utils/generic';
	import ColorScheme from '$lib/components/ColorScheme.svelte';
	import Material from '$lib/components/Material.svelte';
	import { generatePlan, formatOrderOptions } from '$lib/utils/planner';
	import type { Machine } from '$lib/types';
	import { SelectedOrders } from '$lib/stores/SelectedOrders';
	import DataGrid from '$lib/components/DataGrid.svelte';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	export let data;

	let { orders, colors } = data;
	const orderOptions = formatOrderOptions(orders);
	let maxPermSize = 3;
	const machineOptions: { [K in Machine]: string } = {
		butter: 'Butter',
		label: 'Labels',
		embossed_lid: 'Embossed Lids'
	};

	const machineIcons = {
		embossed_lid: 'openmoji:jar',
		label: 'quill:label',
		butter: 'fluent-emoji-high-contrast:butter'
	};

	const machines = Object.keys(machineOptions);
	const machineOptionsForActions: AutocompleteOption[] = Object.keys(machineOptions).map((m) => {
		return {
			label: machineOptions[m],
			value: m
		};
	});
	let availableMachines = machines;

	let loading = false;
	let plan: any = {};
	let error: any = null;

	const makePlan = async () => {
		loading = true;
		plan = {};
		availableMachines.forEach((m) => {
			plan[m] = [];
		});
		error = null;
		try {
			plan = await generatePlan(availableMachines, $SelectedOrders, maxPermSize);
		} catch (e) {
			error = e;
		}
		loading = false;
	};
</script>

<div class="container h-full w-full mx-auto flex flex-col gap-8 py-8 max-sm:px-2 items-center">

	<div class="flex flex-col gap-4 p-4">
		<div class="grid grid-cols-2 flex-row flex-wrap gap-8 justify-center">
			<section class="col-span-2">
				<div class="self-center text-slate-800 text-4xl md:text-4xl pb-2 font-[500]">
					Select Orders to Send to Planner
				</div>
				<!-- <div class=" flex gap-4 sticky top-0 text-2xl text-slate-800 bg-inherit py-2 align-middle">
					<input class="checkbox h-6 w-6 self-center" type="checkbox" on:change={handleSelectAll} />
					<div>Select All</div>
				</div> -->
				<DataGrid
					height="480px"
					tableData={orders}
					machineOptions={machineOptionsForActions}
					{colors}
				/>
			</section>
			<div class="col-span-2 flex gap-8 justify-between align-top flex-wrap">
				<div class="flex gap-4 flex-wrap">
					<div class="card card-hover p-4 flex flex-col gap-2">
						<div class="text-2xl text-slate-800 font-[500]">Machines Available</div>
						<div class="flex gap-2">
							{#each machines as machine}
								<div class="flex items-center hover:border-b-2 hover:border-primary-500">
									<label class="flex gap-2">
										<input
											class="checkbox"
											bind:group={availableMachines}
											checked
											value={machine}
											type="checkbox"
										/>
										<p class="text-slate-800">{machineOptions[machine]}</p>
									</label>
								</div>
							{/each}
						</div>
					</div>
					<div class="card card-hover p-4">
						<p>Maximum Combination Size</p>
						<select class="select" id="max_perm_size" name="max_perm_size" bind:value={maxPermSize}>
							{#each [1, 2, 3, 4, 5, 6] as size}
								<option value={size}>{size}</option>
							{/each}
						</select>
					</div>
				</div>
				<button
					on:click={makePlan}
					class="btn bg-secondary-500 text-white font-bold py-4 self-start rounded-lg"
				>
					Generate Schedule
				</button>
			</div>
		</div>
	</div>
	<section
		id="planner-results"
		class="flex flex-wrap gap-8 w-full justify-between max-h-screen overflow-y-auto p-4"
	>
		{#if error}
			<div class="card p-4 w-full variant-filled-error">
				<div class="text-2xl pb-2">{error.message}</div>
				{#each error.array as err}
					<div class="text-lg">⚠️ {err}</div>
				{/each}
			</div>
		{:else if Object.keys(plan).length > 0}
			{#each Object.entries(plan) as [key, value]}
				<div class="flex flex-col card gap-4 basis-1/3 max-w-md p-4 max-sm:max-w-sm">
					<div class="flex items-center gap-2 text-2xl text-slate-800 p-2">
						{machineOptions[key]}
						<span><Icon icon={machineIcons[key]} /></span>
					</div>
					{#if loading}
						<div class="placeholder animate-pulse rounded-lg h-[600px] w-96" />
					{:else}
						<div class="w-full p-4">
							<Timeline>
								{#each value as v, index}
									{#if v?.type === 'order'}
										<TimelineItem
											title={v.design_name ?? ''}
											timestamp={v.deadline ?? 'No Deadline'}
											badgeText={convertMinutesToHoursMinutes(v.minutes_length) ??
												'Unknown Durarion'}
											description=""
										>
											<div slot="icon">{index + 1}</div>
											<ColorScheme colors={v.color_scheme ?? []} colorMap={colors} />
											<div class="flex flex-row gap-2">
												<div class="text-lg text-slate-800 font-bold">Material:</div>
												<div class="self-center">
													<Material iconHeight="24" material={v.material} />
												</div>
											</div>
										</TimelineItem>
									{:else if v?.type === 'cleanup' || v?.type === 'switch'}
										<TimelineItem
											title={v.type}
											badgeText={convertMinutesToHoursMinutes(v.minutes_length) ??
												'Unknown Durarion'}
											description=""
											height={`${v.minutes_length}`}
										>
											<div slot="icon">{index + 1}</div>
										</TimelineItem>
									{/if}
								{/each}
							</Timeline>
						</div>
					{/if}
				</div>
			{/each}
		{/if}
	</section>
</div>
