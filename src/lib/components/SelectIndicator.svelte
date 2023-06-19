<script lang="ts">
    export let isSelected //: Writable<boolean>;
    export let isSomeSubRowsSelected //: Readable<boolean>;
</script>
  
<input class="checkbox" type="checkbox" bind:checked={$isSelected} indeterminate={$isSomeSubRowsSelected} />