<script lang="ts">
	import { env } from '$env/dynamic/public';
	import { dbToAutocomplete } from '$lib/utils/generic';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import Timeline from '$lib/components/Timeline/Timeline.svelte';
	import TimelineItem from '$lib/components/Timeline/TimelineItem.svelte';
	import Icon from '@iconify/svelte';
	import { convertMinutesToHoursMinutes, capitalizeString } from '$lib/utils/generic';
	import ColorScheme from '$lib/components/ColorScheme.svelte';
	import Material from '$lib/components/Material.svelte';

	export let data;
	let loading = false;

	const machines = ['Labels', 'Butter', 'Embossed Lids'] as const;
	let availableMachines = machines;
	let { orders, employees } = data;
	let plan: {} | { [key in typeof machines[number]]: typeof orders } = {};
	const employeeOptions: AutocompleteOption[] = dbToAutocomplete(employees);

	const machineIcons = {
		'Embossed Lids': 'openmoji:jar',
		Labels: 'quill:label',
		Butter: 'fluent-emoji-high-contrast:butter'
	};

	const generatePlan = async () => {
		const authString = `${env.PUBLIC_OPTIMIZER_USER}:${env.PUBLIC_OPTIMIZER_PASSWORD}`;
		const encodedAuthString = window.btoa(authString);

		const headers = new Headers({
			'Content-Type': 'application/json',
			Authorization: `Basic ${encodedAuthString}`
		});
		loading = true;

		const res = await fetch('http://127.0.0.1:8000/optimize', {
			method: 'POST',
			headers,
			body: JSON.stringify({ machines: availableMachines, orders })
		});
		loading = false;
		const { machines: planMachines, orders: planOrders } = await res.json();

		plan = {};
		plan = planMachines.reduce((acc: any, curr: string) => {
			acc[curr] = planOrders;
			return acc;
		}, plan);
	};
</script>

<div class="container h-full w-full mx-auto flex flex-col gap-4 py-12 max-sm:px-2 items-center">
	<header
		class=" font-bold flex py-2 items-center justify-center mx-auto text-slate-800 text-4xl md:text-6xl"
	>
		Printing Planner 🦾
	</header>
	<div class="flex flex-col gap-4 p-4">
		<div class="flex flex-row flex-wrap gap-4 justify-center">
			<section class="card card-hover shadow-lg rounded-md mx-auto p-4 md:w-96">
				<div class="text-2xl text-slate-800 pb-2">Employees Available</div>
				{#each employeeOptions as employee}
					<label class="flex items-center space-x-2">
						<input class="checkbox" type="checkbox" value={employee.value} checked />
						<p class="text-slate-800 hover:text-primary-500">{employee.label}</p>
					</label>
				{/each}
			</section>
			<section class="card card-hover flex flex-col items-start rounded-md mx-auto p-4 md:w-96">
				<div class="text-2xl text-slate-800 pb-2">Machines Available</div>
				{#each machines as machine}
					<label class="flex items-center space-x-2">
						<input
							class="checkbox"
							bind:group={availableMachines}
							type="checkbox"
							value={machine}
							checked
						/>
						<p class="text-slate-800 hover:text-primary-500">{machine}</p>
					</label>
				{/each}
			</section>
		</div>
		<button on:click={generatePlan} class="btn bg-secondary-500 text-white font-bold">
			Generate Schedule
		</button>
	</div>
	<section class="flex flex-wrap gap-8 justify-center max-h-screen overflow-y-auto">
		{#if Object.keys(plan).length > 0}
			{#each Object.entries(plan) as [key, value]}
				<div class="flex flex-col card gap-4 max-w-md p-4 max-sm:max-w-sm">
					<div class="flex items-center gap-2 text-2xl text-slate-800 p-2">
						{key}
						<span><Icon icon={machineIcons[key]} /></span>
					</div>
					{#if loading}
						<div class="placeholder animate-pulse rounded-lg h-[600px] w-96" />
					{:else}
						<div class="w-full p-4">
							<Timeline>
								{#each value as v, index}
									<TimelineItem
										title={v.design_name ?? ''}
										timestamp={v.deadline ?? 'No Deadline'}
										badgeText={convertMinutesToHoursMinutes(v.minutes_length) ?? 'Unknown Quantity'}
										description=""
									>
										<div slot="icon">{index + 1}</div>
										<ColorScheme colors={v.color_scheme ?? []} />
										<div class="flex flex-row gap-2">
											<div class="text-lg text-slate-800 font-bold">Material:</div>
											<div class="self-center">
												<Material iconHeight="24" material={v.material} />
											</div>
										</div>
									</TimelineItem>
								{/each}
							</Timeline>
						</div>
					{/if}
				</div>
			{/each}
		{/if}
	</section>
</div>
