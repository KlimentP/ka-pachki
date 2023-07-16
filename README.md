# Ka-Pachki

Manufacturing Order Optimization Management System that adds, tracks orders&designs for printing yogurt lids, butter labels, and others, and performs fairly complex optimization of the printing process, given constraints of urgency, time, material, colors, machine/employees availability. 

Built with SvelteKit, Supabase, skeleton-dev, Tailwind. Uses standalone fastapi endpoint for solving the printing optimization problem. 

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.


## Deployment on vercel

You need to specify the env vars: 
```js
PUBLIC_SUPABASE_URL
PUBLIC_SUPABASE_ANON_KEY
PUBLIC_OPTIMIZER_URL_PROD // for python API
PUBLIC_OPTIMIZER_USER // for python API
PUBLIC_OPTIMIZER_PASSWORD // for python API
PUBLIC_PROD = true
```
To skip unnecessary builds, add optimizer dir to ```.vercelignore```
And also in settings/git, add the following: ```git diff --quiet HEAD^ HEAD ./ ':(exclude)optimizer'```


## Deployment of Fastapi Service on GCP
Specify the following env vars (or expose corresponding GCP Secret)
```bash
USERNAME
PASSWORD
PROD = true
```
## Generating Types

Supabase Types:
npx supabase gen types typescript --project-id "PROJECT_ID" --schema public > src/supabase.ts

Generate Zod Types from Supabase Types:
pnpm supabase-to-zod --input src/supabase.ts --output src/schemas.ts

## Functionality Overview
### Planner 

Review outstanding orders and select which one to be sent to planner; tune the planning depending on available machines and complexity of schedule (max number of orders considered for a single machine leads to slower computation time)

![Planner Input](https://github.com/KlimentP/ka-pachki/blob/master/screenshots/planner-input.png?raw=true)

Detailed output of the planner, including order sequence, breakdown of printing duration and breaks due to cleaning/switching printing colors

![Planner Output](https://github.com/KlimentP/ka-pachki/blob/master/screenshots/planner-results.png?raw=true)

### Orders

In additional to standard CRUD functionalities, quick actions menu allows for quick updates

![Action Menu](https://github.com/KlimentP/ka-pachki/blob/master/screenshots/action-menu.png?raw=true)

![Action Form](https://github.com/KlimentP/ka-pachki/blob/master/screenshots/action-form.png?raw=true)

### Customers 
![Customers](https://github.com/KlimentP/ka-pachki/blob/master/screenshots/customers.png?raw=true)

### Designs 
![Designs](https://github.com/KlimentP/ka-pachki/blob/master/screenshots/designs.png?raw=true)

![Create Color](https://github.com/KlimentP/ka-pachki/blob/master/screenshots/create-color.png?raw=true)
