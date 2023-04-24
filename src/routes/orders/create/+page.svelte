<script lang="ts">
	import AutoCompleteSingle from '$lib/components/AutoCompleteSingle.svelte';
	import type { AutocompleteOption } from '@skeletonlabs/skeleton';

	let customerOptions: AutocompleteOption[] = [
		{ value: 'rodopea', label: 'Rodopea' },
		{ value: 'bor_chvor', label: 'Bor Chvor' },
		{ value: 'madjarov', label: 'Madjarov' },
		{ value: 'kravarkata', label: 'Kravarkata' },
		{ value: 'verea', label: 'Verea' },
	];
    let designOptions: AutocompleteOption[] = [
		{ value: 'mleko', label: 'Mleko' },
		{ value: 'mazno_mleko', label: 'Mazno Mleko' },
		{ value: 'niskomasleno_mleko', label: 'Niskomasleno Mleko' },
		{ value: 'kravarkata_v_ugula', label: 'Kravarkata v Ugula' },
		{ value: 'dedo_liben', label: 'Dedo Liben' },
	];
</script>

<div class="container h-full mx-auto flex flex-col justify-center items-center max-sm:p-4">
	<h2 class="mb-2">Create Order</h2>
	<form class="w-full max-w-lg">
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
				<AutoCompleteSingle options={customerOptions} />
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
				<AutoCompleteSingle options={designOptions} />
			</div>
		</div>
		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="qty">
					Quantity
				</label>
				<input class="input" id="qty" type="number" placeholder="Quantity" />
			</div>
		</div>

		<div class="flex flex-wrap -mx-3 mb-6">
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
					value="Lid"
				>
					<option value="Lid">Lid</option>
					<option value="Label">Label</option>
					<option value="Butter">Butter</option>
					<option value="Embossed Lid">Embossed Lid</option>
				</select>
			</div>
		</div>

		<div class="flex flex-wrap -mx-3 mb-6">
			<div class="w-full px-3">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="status"
				>
					Status
				</label>
				<select class="select" id="status" value="Scheduled">
					<option value="Scheduled">Scheduled</option>
					<option value="In progress">In progress</option>
					<option value="Completed">Completed</option>
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
				<input class="input" id="units-produced" type="number" placeholder="Units Produced" />
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
					<select class="select" id="urgent">
						<option value="No">No</option>
						<option value="Yes">Yes</option>
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
				<input class="input" id="deadline" type="date" />
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
				<textarea class="textarea" id="notes" placeholder="Notes" />
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
