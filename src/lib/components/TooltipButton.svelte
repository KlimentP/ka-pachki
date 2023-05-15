<script lang="ts">
	import type { PopupSettings } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';

	export let popupText = '';
	export let target = '';
	if (!target) {
		target =
			Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
	}
	let popupSettings: PopupSettings = {
		// Set the event as: click | hover | hover-click | focus | focus-click
		event: 'hover',
		placement: 'top',
		// Provide a matching 'data-popup' value.
		target,
		closeQuery: ''
	};
</script>

<div>
	<div use:popup={popupSettings}>
		<slot name="button" />
	</div>
	<div data-popup={target}>
		<slot name="tooltip">
			<div
				class="bg-slate-200 p-4 rounded-lg border-2
			align-middle mx-auto justify-center items-center shadow-lg"
			>
				{popupText}
			</div>
		</slot>
	</div>
</div>
