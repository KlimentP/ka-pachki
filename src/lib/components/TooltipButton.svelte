<script lang="ts">
	import type { PopupSettings } from '@skeletonlabs/skeleton';
	import { popup } from '@skeletonlabs/skeleton';

	export let popupText = '';
    export let target: string;
	let popupSettings: PopupSettings = {
		// Set the event as: click | hover | hover-click | focus | focus-click
		event: 'hover' ,
		placement: 'top',
		// Provide a matching 'data-popup' value.
		target,
		closeQuery: '',
	};
</script>

<div>
	<div use:popup={popupSettings}>
		<slot name="button"></slot>
	</div>
	<div data-popup={target}>
		<slot name="tooltip">{popupText}</slot>
	</div>
</div>
