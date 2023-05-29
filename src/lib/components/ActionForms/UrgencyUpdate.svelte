<script lang="ts">
	import { modalStore } from '@skeletonlabs/skeleton';
	import BaseActionForm from './BaseActionForm.svelte';
	const { selectedOrder } = $modalStore[0].meta;
	export let action: string;
</script>

<BaseActionForm {action}>
	<div class="w-full px-3">
		<div class="w-full px-3">
			<div class="relative">
				<label
					class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
					for="urgent"
				>
					Urgent
				</label>
				<select
					class="select"
					id="urgent"
					name="urgent"
                    value={selectedOrder?.urgent.toString()}
				>
					<option value="false">No</option>
					<option value="true">Yes</option>
				</select>
				<div
					class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
				>
					<svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
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
</BaseActionForm>
