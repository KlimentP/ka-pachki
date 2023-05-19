import { env } from '$env/dynamic/public';

export const generatePlan = async (availableMachines: any, selectedOrders: any, plan: any) => {
	plan = {};
	const authString = `${env.PUBLIC_OPTIMIZER_USER}:${env.PUBLIC_OPTIMIZER_PASSWORD}`;
	const encodedAuthString = window.btoa(authString);
	const headers = new Headers({
		'Content-Type': 'application/json',
		Authorization: `Basic ${encodedAuthString}`
	});

	const res = await fetch(`${env.PUBLIC_OPTIMIZER_URL}/optimize`, {
		method: 'POST',
		headers,
		body: JSON.stringify({ machines: availableMachines, orders: selectedOrders })
	});

	const { machines: planMachines, orders: planOrders } = await res.json();
	plan = planMachines.reduce((acc: any, curr: string) => {
		acc[curr] = planOrders;
		return acc;
	}, plan);
	console.log(plan);
	return plan;
};

export const formatOrderOptions = (orders: any) => {
	return orders.map((order) => ({
		label: `${order.design_name} - ${order.units_already_produced}/${order.quantity} produced -  ${
			order.material
		} - ${order.minutes_length} minutes  ${order.deadline ?? ''}`,
		value: order
	}));
};
