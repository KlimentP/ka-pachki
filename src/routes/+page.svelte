
<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div>
		{#if data.session}
			<div class="container h-full mx-auto flex justify-center items-center">
				<div class="space-y-5">
					<h1>Hello {data.session.user.email}</h1>
				</div>
			</div>
		{/if}
	</div>
</div>

