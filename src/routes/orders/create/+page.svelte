<script lang="ts">
	import AutoCompleteSingle from '$lib/components/AutoCompleteSingle.svelte';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';
	import { dbToAutocomplete, capitalizeString } from '$lib/utils/generic';
	import { fade } from 'svelte/transition';
	export let data;
	export let form;

	let customerOptions: AutocompleteOption[] = dbToAutocomplete(data.customers);
	let designOptions: AutocompleteOption[] = dbToAutocomplete(data.designs);
	let employeeOptions: AutocompleteOption[] = dbToAutocomplete(data.employees);

</script>

<div class="container h-full mx-auto flex flex-col gap-4 justify-center items-center max-sm:p-4">
	<h2 class="mb-2">Create Order</h2>
	{#if form?.errors}
		<aside
			transition:fade|local={{ duration: 500 }}
			class="alert variant-filled-error w-full max-w-lg"
		>
			<!-- Message -->
			<div class="alert-message">
				<h3>Error</h3>
				{#each Object.entries(form.errors) as [key, value]}
					<p>{capitalizeString(key)}: {value}</p>
				{/each}
			</div>
		</aside>
	{/if}
	<form class="w-full max-w-lg" method="POST">
		<!-- <div class="flex flex-wrap -mx-3 mb-6">
          <div class="w-full px-3">
            <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="date-updated">
              Date Updated
            </label>
            <input class="" id="date-updated" type="date" placeholder="Date Updated">
          </div>
        </div>
        <div class="flex flex-wrap -mx-3 mb-6">
          <div class="w-full px-3">
            <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="date-closed">
              Date Closed
            </label>
            <input class="" id="date-closed" type="date" placeholder="Date Closed">
          </div>
        </div> -->
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="customer-id"
				>
					Customer
				</label>
				<AutoCompleteSingle options={customerOptions} formName="customer_id" />
			</div>
		</div>

		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="design"
				>
					Design
				</label>
				<AutoCompleteSingle options={designOptions} formName="design_id" />
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="qty">
					Quantity
				</label>
				<input
					required
					class="input"
					id="quantity"
					type="number"
					name="quantity"
					placeholder="Quantity"
					value={form?.quantity ?? 0}
				/>
			</div>
		</div>

		<!-- <div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Material
				</label>
				<select
					class="select block appearance-none w-full bg-sky-100 border border-gray-200 text-gray-700 py-3 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
					id="material"
					size="4"
					name="material"
					value={form?.material ?? 'lid'}
				>
					<option value="lid">Lid</option>
					<option value="label">Label</option>
					<option value="butter">Butter</option>
					<option value="embossed_lid">Embossed Lid</option>
				</select>
			</div>
		</div> -->

		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="status"
				>
					Status
				</label>
				<select class="select" id="status" name="status" value={form?.status ?? 'scheduled'}>
					<option value="scheduled">Scheduled</option>
					<option value="in_progress">In progress</option>
					<option value="completed">Completed</option>
				</select>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="units-produced"
				>
					Units Already Produced
				</label>
				<input
					class="input"
					id="units-produced"
					name="units_already_produced"
					type="number"
					value={form?.units_already_produced ?? 0}
				/>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="material"
				>
					Specifically Assign Employee
				</label>
				<select class="select" name="assigned_employee" size="4" value={form?.assigned_employee ?? ""}>
					{#each employeeOptions as employee}
						<option value={employee.value}>{employee.label}</option>
					{/each}
				</select>
			</div>
		</div>

		<!-- <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full px-3">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="created-by">
                Created By
              </label>
              <input class="" id="created-by" type="text" placeholder="Created By">
            </div>
          </div> -->
		<!-- <div class="flex flex-wrap -mx-3 mb-6">
            <div class="w-full px-3">
              <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="closed-by">
                Closed By
              </label>
              <input class="" id="closed-by" type="text" placeholder="Closed By">
            </div>
          </div> -->
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<div class="relative">
					<label
						class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
						for="urgent"
					>
						Urgent
					</label>
					<select class="select" id="urgent" name="urgent" value={form?.urgent ?? 'false'}>
						<option value="false">No</option>
						<option value="true">Yes</option>
					</select>
					<div
						class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
					>
						<svg
							class="fill-current h-4 w-4"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
						>
							<path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
							<path
								fill-rule="evenodd"
								d="M10 18a8 8 0 100-16 8 8 0 000 16zm0-2a6 6 0 100-12 6 6 0 000 12z"
							/>
						</svg>
					</div>
				</div>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="deadline"
				>
					Deadline
				</label>
				<input
					class="input"
					id="deadline"
					type="date"
					name="deadline"
					value={form?.deadline ?? ''}
				/>
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="notes"
				>
					Notes
				</label>
				<textarea class="textarea" id="notes" name="notes" value={form?.notes ?? ''} />
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<!-- <div class="w-full px-3">
                          <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="order-id">
                            Order ID
                          </label>
                          <input class="" id="order-id" type="text" placeholder="Order ID">
                        </div>
                      </div> -->
			<div class="flex flex-wrap -mx-3 mb-2">
				<div class="w-full px-3">
					<button
						class="bg-primary-500 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
						type="submit"
					>
						Submit
					</button>
				</div>
			</div>
		</div>
	</form>
</div>
