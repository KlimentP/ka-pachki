
<script lang="ts">
	import DesignsList from '$lib/components/DesignsList.svelte';

	export let data;
	let {tableData} = data;


	</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<DesignsList items={tableData} />
</div>
