<script lang="ts">
	// The ordering of these imports is critical to your app working properly
	import '@skeletonlabs/skeleton/themes/theme-skeleton.css';
	// If you have source.organizeImports set to true in VSCode, then it will auto change this ordering
	import '@skeletonlabs/skeleton/styles/all.css';
	// Most of your app wide CSS should be put in this file
	import '../app.postcss';
	import { invalidate } from '$app/navigation';
	import { onMount } from 'svelte';
	import type { LayoutData } from './$types';

	export let data: LayoutData;

	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import ComboBox from '$lib/components/ComboBox.svelte';
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	import { capitalizeString } from '$lib/utils/generic';
	import { page } from '$app/stores';

	$: ({ supabase, session } = data);

	function signout() {
		supabase.auth.signOut();
	}
	onMount(() => {
		const { data } = supabase.auth.onAuthStateChange((event, _session) => {
			if (_session?.expires_at !== session?.expires_at) {
				invalidate('supabase:auth');
			}
		});

		return () => data.subscription.unsubscribe();
	});

	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	const resources = ['customers', 'designs', 'orders', 'colors']

	const dropdowns = {};

	resources.forEach(( name ) => {
		dropdowns[name] = [
			{ url: `/${name}/create`, label: `Add ${name}` },
			{ url: `/${name}`, label: `View ${name}` }
		];
	});
	dropdowns["designs"] = [...dropdowns["designs"], ...dropdowns["colors"]];
	dropdowns["orders"] = [...dropdowns["orders"], ...dropdowns["customers"]];
	delete dropdowns["colors"];
	delete dropdowns["customers"];
	
</script>

<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar
			slotDefault="w-0"
			padding="max-sm:py-2 md:p-2"
			gap="gap-1 md:gap-4"
			background="bg-slate-950"
		>
			<svelte:fragment slot="lead">
				<div class="text-surface-900-50--token">
					<a href="/" aria-label="Home Page" class="text-white">
						<img
							class="h-8 md:h-14 hover:border-b-2 border-orange-500 p-1"
							src="/fleks-ko-logo-medium.png"
							alt="Fleks Ko Logo"
						/>
					</a>
				</div>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<div class="flex items-center gap-1 md:gap-2">
					{#if $page.data.session}
						<a
							href="/planner"
							class="btn btn-sm variant-soft-secondary text-slate-300 hover:text-secondary-500"
							>Planner</a
						>
						{#each Object.keys(dropdowns) as name}
							<ComboBox comboboxValue={capitalizeString(name)} listItems={dropdowns[name]} />
						{/each}
						<!-- <ComboBox comboboxValue={'Designs'} listItems={designDropdown} />
						<ComboBox comboboxValue={'Orders'} listItems={ordersDropdown} /> -->
						<button
							type="button"
							class="btn btn-sm  text-slate-300 hover:text-primary-500"
							on:click={signout}>Sign Out</button
						>
					{:else}
						<a href="/login" class="btn btn-sm text-slate-300 hover:text-primary-500">Sign In</a>
					{/if}
					<!-- <LightSwitch /> -->
				</div></svelte:fragment
			>
		</AppBar>
	</svelte:fragment>
	<slot />
	<footer class="py-4 shadow-lg bg-slate-950 max-sm:mt-12 max-sm:px-4">
		<div class="container mx-auto flex items-center justify-between">
			<div class="flex items-center">
				<div class="mr-4 text-white">Flex Ko</div>
			</div>
		</div>
	</footer>
</AppShell>
