<script lang="ts">
	import Timeline from '$lib/components/Timeline/Timeline.svelte';
	import TimelineItem from '$lib/components/Timeline/TimelineItem.svelte';
	import Icon from '@iconify/svelte';
	import { convertMinutesToHoursMinutes } from '$lib/utils/generic';
	import ColorScheme from '$lib/components/ColorScheme.svelte';
	import Material from '$lib/components/Material.svelte';
	import { generatePlan, formatOrderOptions } from '$lib/utils/planner';
	import type { Machine } from '$lib/types';

	export let data;

	let { orders, colors } = data;
	// let employeeOptions = employees.map((e) => {
	// 	return {
	// 		label: e?.name,
	// 		value: e?.name
	// 	};
	// });
	const orderOptions = formatOrderOptions(orders);
	let selectedOrders = orders;
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
	let availableMachines = machines;

	let loading = false;
	let plan: any = {};
	let error: any = null;

	const handleSelectAll = (event: any) => {
		if (event.target.checked) {
			selectedOrders = orders;
		} else {
			selectedOrders = [];
		}
	};
	const makePlan = async () => {
		loading = true;
		plan = {};
		error = null;
		try {
			plan = await generatePlan(availableMachines, selectedOrders, maxPermSize);
		} catch (e) {
			error = e;
		}
		loading = false;
	};
</script>

<div class="container h-full w-full mx-auto flex flex-col gap-4 py-4 max-sm:px-2 items-center">
	<header
		class=" font-bold flex py-2 items-center justify-center mx-auto text-slate-800 text-4xl md:text-6xl"
	>
		Let's Plan Some Printing 🦾
	</header>
	<div class="flex flex-col gap-4 p-4">
		<div class="grid grid-cols-2 flex-row flex-wrap gap-8 justify-center">
			<section class="col-span-2 card card-hover shadow-lg rounded-md px-4 pb-4 h-[480px] overflow-auto">
				<div class=" flex gap-4 sticky top-0 text-2xl text-slate-800 bg-inherit py-4 align-middle">
					<input
						class="checkbox h-6 w-6 self-center"
						type="checkbox"
						checked
						on:change={handleSelectAll}
					/>
					<div>Which Orders to Send to Planner?</div>
				</div>
				{#each orderOptions as order}
					<label
						class="flex items-center space-x-2 tracking-wide mb-2"
						class:!bg-amber-300={order.value?.urgent}
					>
						<input
							class="checkbox"
							type="checkbox"
							value={order.value}
							bind:group={selectedOrders}
						/>
						<p class="text-slate-800 hover:text-primary-500">{order.label}</p>
					</label>
				{/each}
			</section>
			<!-- <section class="card card-hover shadow-lg rounded-md mx-auto p-4 md:w-96">
				<div class="text-2xl text-slate-800 pb-2">Employees Available</div>
				{#each employeeOptions as employee}
					<label class="flex items-center space-x-2">
						<input
							class="checkbox"
							type="checkbox"
							bind:group={availableEmployees}
							value={employee.value}
						/>
						<p class="text-slate-800 hover:text-primary-500">{employee.label}</p>
					</label>
				{/each}
			</section> -->
			<div
				class="col-span-2 w-full flex flex-col gap-2 justify-between card card-hover rounded-md p-4"
			>
				<!-- <div class="flex gap-16 md:gap-48 align-middle py-2"> -->
				<!-- <p class="text-slate-800 hover:text-primary-500 w-36 self-center">Assigned Employee</p> -->

				<!-- </div> -->
				<div class="flex gap-4 justify-between align-top">
					<div class="flex flex-col gap-2">
						<div class="text-2xl text-slate-800">Machines Available</div>
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
					<div class="">
						<p>Maximum Combination Size</p>
						<select class="select" id="max_perm_size" name="max_perm_size" bind:value={maxPermSize}>
							{#each [1, 2, 3, 4, 5, 6] as size}
								<option value={size}>{size}</option>
							{/each}
						</select>
					</div>
					<button
						on:click={makePlan}
						class="btn bg-secondary-500 text-white font-bold h-12 self-center"
					>
						Generate Schedule
					</button>
				</div>
			</div>
		</div>
	</div>
	<section
		id="planner-results"
		class="flex flex-wrap gap-8 justify-center max-h-screen overflow-y-auto py-2"
	>
		{#if error}
			<div class="card p-4 w-full variant-filled-error">
				<div class="text-2xl pb-2">{error.message}</div>
				{#each error.array as err}
					<div class="text-lg">{err}</div>
				{/each}
			</div>
		{:else if Object.keys(plan).length > 0}
			{#each Object.entries(plan) as [key, value]}
				<div class="flex flex-col card gap-4 max-w-md p-4 max-sm:max-w-sm">
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
