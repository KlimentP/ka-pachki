<script lang="ts">
	export let data;
	let { tableData } = data;

	// let filter = '';
	// let filteredData = tableData;
	const keysToFilter = ["date_created", "status", "customer_name", "quantity", "design_name", "material", "color_scheme", "deadline", "design_name"];

	function filterObjectByKeys(obj, keys) {
	return keys.reduce((result, key) => {
		if (obj.hasOwnProperty(key)) {
		result[key] = obj[key];
		}
		return result;
	}, {});
	}

	const filteredData = tableData.map((obj) => filterObjectByKeys(obj, keysToFilter));
	const headers = Object.keys(filteredData[0] || {});

	// function handleFilterChange(event) {
	// 	filter = event.target.value;
	// 	filteredData = tableData.filter((item) =>
	// 		Object.values(item).some((value) =>
	// 			value?.toString().toLowerCase().includes(filter.toLowerCase())
	// 		)
	// 	);
	// }

	// function handleEdit(index) {
	// 	// Add your edit functionality here
	// }

	// function handleDelete(index) {
	// 	tableData.splice(index, 1);
	// 	tableData = [...tableData];
	// }
</script>

<div class="container h-full mx-auto flex flex-col gap-4 justify-center items-center">
	<!-- <input type="text" placeholder="Filter" bind:value={filter} on:input={handleFilterChange} /> -->
	<div class="table-container hover:border-2 border-primary-400 ">
		<table class="table table-comfortable table-hover table-auto bg-primary-200 text-slate-800">
			<thead class="text-primary-400 !bg-slate-900">
				<tr>
					<!-- Add table headers for each field here -->
					<th>Actions</th>
					{#each headers as header}
						<th >{header}</th>
					{/each}
				</tr>
			</thead>
			<tbody>
				{#each filteredData as item, index}
					<tr>
						<td>
							Coming Soon!
							<!-- <button on:click={() => handleEdit(index)}>Edit</button>
							<button on:click={() => handleDelete(index)}>Delete</button> -->
						</td>
						{#each Object.values(item) as value}
							<td>{value || ''}</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
