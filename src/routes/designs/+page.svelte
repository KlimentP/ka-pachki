
<script lang="ts">

	import ItemList from '$lib/components/ItemLists/ItemList.svelte';
	import DesignItemBody from '$lib/components/ItemLists/DesignItemBody.svelte';
	export let form;
	export let data;
	let {tableData} = data;


	</script>
<div class="container h-full mx-auto flex justify-center">
	<ItemList items={tableData} itemType="design" {form}>
	<svelte:fragment let:item={item} slot="item-body">
		<DesignItemBody {item} />
	</svelte:fragment>
	</ItemList>
</div>
