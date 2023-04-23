<script lang="ts">
	// The ordering of these imports is critical to your app working properly
	import '@skeletonlabs/skeleton/themes/theme-skeleton.css';
	// If you have source.organizeImports set to true in VSCode, then it will auto change this ordering
	import '@skeletonlabs/skeleton/styles/all.css';
	// Most of your app wide CSS should be put in this file
	import '../app.postcss';
	import { AppShell, AppBar, LightSwitch } from '@skeletonlabs/skeleton';
	import ComboBox from '$lib/components/ComboBox.svelte';
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import { storePopup } from '@skeletonlabs/skeleton';
	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
	const designDropdown = [
		{ url: '/designs/create', label: 'Create' },
		{ url: '/designs', label: 'View' }
	];
	const ordersDropdown = [
		{ url: '/orders/create', label: 'Create' },
		{ url: '/orders', label: 'View'}		 
	];
</script>

<AppShell>
	<svelte:fragment slot="header">
		<!-- App Bar -->
		<AppBar background="bg-surface-800">
			<svelte:fragment slot="lead">
				<div class="text-surface-900-50--token">
					<a href="/" aria-label="Home Page" class="text-black dark:text-white"> 
						<img class="h-12 " src="/fleks-ko-logo-medium.png" alt="Fleks Ko Logo"/>
					 </a>
				</div>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<div class="flex items-center gap-2">
					<ComboBox comboboxValue={'Designs'} listItems={designDropdown} />
					<ComboBox comboboxValue={'Orders'} listItems={ordersDropdown} />

					<!-- <LightSwitch /> -->
				</div></svelte:fragment
			>
		</AppBar>
	</svelte:fragment>
	<slot />
	<footer class="py-4 shadow-lg bg-surface-800 max-sm:mt-12 max-sm:px-4">
		<div class="container mx-auto flex items-center justify-between">
			<div class="flex items-center">
				<div class="mr-4 text-white">Flex Ko</div>
			</div>
		</div>
	</footer>
</AppShell>
