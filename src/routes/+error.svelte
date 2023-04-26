<script>
	import { page } from '$app/stores';
</script>

<div
	class="container h-full mx-auto flex flex-col gap-4 justify-center items-center max-sm:p-4"
>       <h1 class="text-slate-800">UH OH</h1>
		<h2 class="text-slate-800 italic">{$page.status} {$page?.error?.message}</h2>
		<span class="text-xl">
			<img class="h-96 rounded-lg" src="/error.png" alt={$page.status.toString()} />
		</span>
</div>
