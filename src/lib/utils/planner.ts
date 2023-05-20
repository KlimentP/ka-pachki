import { env } from '$env/dynamic/public';

export const generatePlan = async (availableMachines: any, selectedOrders: any) => {
	const authString = `${env.PUBLIC_OPTIMIZER_USER}:${env.PUBLIC_OPTIMIZER_PASSWORD}`;
	const encodedAuthString = window.btoa(authString);
	const headers = new Headers({
		'Content-Type': 'application/json',
		Authorization: `Basic ${encodedAuthString}`
	});
    const url = env.PUBLIC_PROD === 'true' ? `${env.PUBLIC_OPTIMIZER_URL_PROD}/optimize` : `${env.PUBLIC_OPTIMIZER_URL_DEV}/optimize`;
    let res;
    try {
        res = await fetch(url, {
            method: 'POST',
            headers,
            body: JSON.stringify({ machines: availableMachines, orders: selectedOrders })
        });
    } catch (error) {
        console.log(error);
        throw new Error('Error generating plan');
    }
	return await res.json();
};

export const formatOrderOptions = (orders: any) => {
	return orders.map((order) => ({
		label: `${order.design_name} - ${order.units_already_produced}/${order.quantity} produced -  ${
			order.material
		} - ${order.minutes_length} minutes  ${order.deadline ?? ''}`,
		value: order
	}));
};
