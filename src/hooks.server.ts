import {
    PUBLIC_SUPABASE_URL,
    PUBLIC_SUPABASE_ANON_KEY
  } from '$env/static/public';
  import { createSupabaseServerClient } from '@supabase/auth-helpers-sveltekit';
  import { redirect, type Handle } from '@sveltejs/kit';

  export const handle: Handle = async ({ event, resolve }) => {
    event.locals.supabase = createSupabaseServerClient({
      supabaseUrl: PUBLIC_SUPABASE_URL,
      supabaseKey: PUBLIC_SUPABASE_ANON_KEY,
      event
    });
  
    /**
     * A convenience helper so we can just call await getSession() instead const { data: { session } } = await supabase.auth.getSession()
     */
    event.locals.getSession = async () => {
      const {
        data: { session }
      } = await event.locals.supabase.auth.getSession();
      return session;
    };
    if (event.url.pathname !== '/signup' && event.url.pathname !== '/login' && event.url.pathname !== '/' ) {
      const session = await event.locals.getSession();
      if (!session) {
        throw redirect(303, '/login')
      }
    }
    return resolve(event, {
      /**
       * There´s an issue with `filterSerializedResponseHeaders` not working when using `sequence`
       *
       * https://github.com/sveltejs/kit/issues/8061
       */
      filterSerializedResponseHeaders(name) {
        return name === 'content-range';
      }
    });
  };