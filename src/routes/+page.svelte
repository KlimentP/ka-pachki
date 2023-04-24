
<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div>
		{#if data.session}
			<div class="container h-full mx-auto flex justify-center items-center">
				<div class="space-y-5">
					<h1 class="mb-2">Hello {data.session.user.email}</h1>
				</div>
			</div>
		{:else}
			<div class="container h-full mx-auto flex justify-center items-center">
				<div class="space-y-5">
					<h1 class="mb-2">Hello Guest</h1>
				</div>
			</div>
		{/if}
		<img class="rounded-xl shadow-lg"src="hero.png" alt="Magic printing press"/>
	</div>
</div>

