import { supabaseClient } from '$lib/supabaseClient';
import { calculateMinutesLength } from '../materialCalcs';
import type { Material } from '$lib/types';

import type { Database } from '../../../supabase';

type CalcedOrder = Database['public']['Views']['orders_full']['Row'] & {
	minutes_length: number;
	days_remaining: number;
	material: Material;
};

function calculateDaysRemaining(obj: any) {
    if (obj.date_created && obj.deadline) { 
        const date_created = new Date(obj.date_created);
        const deadline = new Date(obj.deadline);

        const timeDifference = deadline.getTime() - date_created.getTime();

        // There are 1000 milliseconds in a second, 60 seconds in a minute, 
        // 60 minutes in an hour, and 24 hours in a day, so we divide by those values.
        return Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    }
    else {
        // One or both dates are null, return null
        return null;
    }
}

export async function selectOrders() {
	const { data: orders } = (await supabaseClient
		.from('orders_full')
		.select('*')
		.order('quantity', { ascending: false }));

	// substract units_already_produced from quantity to get the remaining units to produce and then convert to minutes
	orders?.map((order) => {
		const unitsRemaining = (order.quantity ?? 0) - (order.units_already_produced ?? 0);
		order.minutes_length =
			order.quantity && order.material && unitsRemaining > 0
				? calculateMinutesLength(
						order.quantity - (order.units_already_produced ?? 0),
						order.material
				  )
				: 0;
		order.name = order.design_name;
		order.days_remaining = calculateDaysRemaining(order);
		return order;
	});
	return orders;
}
