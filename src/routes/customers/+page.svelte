<script lang="ts">
	import ItemList from '$lib/components/ItemLists/ItemList.svelte';
	import CustomerItemBody from '$lib/components/ItemLists/CustomerItemBody.svelte';
	export let form;
	export let data;
	const { tableData } = data;
</script>

<div class="flex flex-row flex-wrap gap-8 container h-full mx-auto justify-center items-center p-4">
	<ItemList items={tableData} itemType="customer" {form}>
		<svelte:fragment let:item slot="item-body">
			<CustomerItemBody {item} />
		</svelte:fragment>
	</ItemList>
</div>
