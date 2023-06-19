import { env } from '$env/dynamic/public';
import { error } from '@sveltejs/kit';
class CustomError extends Error {
	array: any[];
    constructor(message: string, array: any[]) {
        super(message); // Call parent constructor with the message parameter
        this.name = 'CustomError'; // Set the name property to the name of this class
        this.array = array; // Store the array
    }
}

interface CheckResult {feasible: boolean, message?: string, errorArray?: any[]}

function factorialize(num: number) {
	if (num === 0 || num === 1) {
   return 1;
 }
	for (let i = num - 1; i >= 1; i--) {
	  num *= i;
	}
	return num;
  }

const materialToMachine = {
	butter: 'butter', 
	embossed_lid: 'embossed_lid',
	label: 'label',
	uv_butter: 'label'
}

const checkUrgentFits = (urgentOrders: any, availableMachines: any): CheckResult =>{
	const issues = [];
	for (const order of urgentOrders) {
		if (order.machine && !availableMachines.includes(order.machine)) {
			issues.push( `Order ${order.design_name} - ${order.quantity} is assigned to machine ${order.assigned_machine_id} 
			but that machine is not available.`);
		}
		if (order.material !== 'lid' && !availableMachines.includes(materialToMachine[order.material])) {
			issues.push( `Order ${order.design_name} - ${order.quantity} is made of material ${order.material} 
			but that machine is not available.`);
		}
	}
	if (issues.length > 0) {
		return {feasible: false, message: 'Issues with urgent orders', errorArray: issues};
	}
	return {feasible: true};
}

const checkUrgentHours = (urgentOrders: any, availableMachines: any): CheckResult =>{
	const issues = [];
	const availableMinutes = availableMachines.length * 410;
	const urgentMinutes = urgentOrders.reduce((acc: number, order: any) => acc + order.minutes_length, 0);
	if (urgentMinutes > availableMinutes) {
		issues.push(`There are ${urgentMinutes} minutes of urgent orders but only ${availableMinutes} minutes available.`);
	}
	for (const machine of availableMachines) {
		const machineOrders = urgentOrders.filter((order: any) => order.machine === machine || materialToMachine[order.material] === machine);
		const duration = machineOrders.reduce((acc: number, order: any) => acc + order.minutes_length, 0);
		if (duration > 410) {
			issues.push(`Machine ${machine} is assigned ${duration} minutes of work but can only work 480 minutes.`);
		}

	}
	if (issues.length > 0) {
		return {feasible: false, message: 'Too many urgent orders', errorArray: issues};
	}
	return {feasible: true};
}

const checkPlanFeasibility = (availableMachines: any,
	selectedOrders: any,
	maxPermSize: number) : CheckResult => {

		const permutationsCount = factorialize(selectedOrders.length)/(factorialize(selectedOrders.length - maxPermSize));
		if (permutationsCount > 10000000) {
			return {feasible: false, message: `There are too many potential permutations. 
			Please select fewer orders or decrease the maximum permutation size.`, errorArray: []};
		}
		const urgentOrders = selectedOrders.filter((order: any) => order.urgent);
		let feasible, message, errorArray;
		({feasible, message, errorArray} = checkUrgentFits(urgentOrders, availableMachines));
		if (feasible === false && message && errorArray) {
			return {feasible: false, message, errorArray};
		}
		({feasible, message, errorArray} = checkUrgentHours(urgentOrders, availableMachines));
		if (feasible === false && message && errorArray) {
			return {feasible: false, message, errorArray};
		}
		return {feasible: true};
	}

export const generatePlan = async (
	availableMachines: any,
	selectedOrders: any,
	maxPermSize: number,

	// selectedEmployees: any
) => {
	const {feasible, message, errorArray} = checkPlanFeasibility(availableMachines, selectedOrders, maxPermSize);
	if (feasible === false && message && errorArray) {
		throw new CustomError(message, errorArray);
	}
	const authString = `${env.PUBLIC_OPTIMIZER_USER}:${env.PUBLIC_OPTIMIZER_PASSWORD}`;
	const encodedAuthString = window.btoa(authString);
	const headers = new Headers({
		'Content-Type': 'application/json',
		Authorization: `Basic ${encodedAuthString}`
	});
	const url =
		env.PUBLIC_PROD === 'true'
			? `${env.PUBLIC_OPTIMIZER_URL_PROD}/optimize`
			: `${env.PUBLIC_OPTIMIZER_URL_DEV}/optimize`;
	let res;

	try {
		res = await fetch(url, {
			method: 'POST',
			headers,
			body: JSON.stringify({
				machines: availableMachines,
				orders: selectedOrders,
				max_perm_size: maxPermSize,
			})
		});
	} catch (error) {
		throw new CustomError('Error generating plan', []);
	}
	return await res.json();
};

export const formatOrderOptions = (orders: any) => {
	return orders.map((order: any) => ({
		label: `${order.design_name} - ${order.units_already_produced}/${order.quantity} produced -  ${
			order.material
		} - ${order?.minutes_length} minutes - ${order.machine}  due in ${
			order?.days_remaining ?? '?'
		} days`,
		value: order
	}));
};
