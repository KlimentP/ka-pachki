
<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="container h-full mx-auto flex justify-center items-center py-10">
    <div class="relative h-3/5 w-3/5 bg-cover bg-center rounded-xl shadow-lg overflow-hidden" style="background-image: url('hero.png');">
        <div class="bg-black bg-opacity-60 h-full w-full flex flex-col items-center justify-center p-10">
            {#if data.session}
                <div class="space-y-5">
                    <h1 class="text-4xl mb-2 text-slate-200 font-bold">Hello </h1>
					<div class="text-3xl text-slate-200">{data.session.user.email}</div>
					<a href="/planner"  class="btn bg-transparent border-2 border-white !text-slate-200 hover:!text-secondary-500 hover:border-secondary-500 hover:bg-secondary-500 hover:bg-opacity-20 font-bold py-2 px-4 rounded">Go to planner</a>
                </div>
            {:else}
                <div class="space-y-5">
                    <h1 class="text-4xl mb-2 text-slate-200 font-bold">Hello Guest</h1>
					<a href="/login"  class="btn bg-transparent border-2 border-white !text-slate-200 hover:text-gray-100 font-bold py-2 px-4 rounded">Sign in</a>
                </div>
            {/if}
            <div class="flex justify-center space-x-5">
            </div>
        </div>
    </div>
</div>

