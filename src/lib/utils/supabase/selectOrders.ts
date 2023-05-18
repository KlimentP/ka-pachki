import { supabaseClient } from '$lib/supabaseClient';
import { calculateMinutesLength } from '../materialCalcs';
import type { Material } from "$lib/types";

import type { Database } from '../../../supabase';

type CalcedOrder = Database['public']['Views']['orders_full']['Row'] & {
    minutes_length: number;
    material: Material;
  }

export async function selectOrders() {
	const { data: orders }  = await supabaseClient.from('orders_full').select('*') as {data: CalcedOrder[]};
    // substract units_already_produced from quantity to get the remaining units to produce and then convert to minutes
	orders?.map((order) => {
		const unitsRemaining = (order.quantity ?? 0) - (order.units_already_produced ?? 0);
		order.minutes_length = order.quantity && order.material && unitsRemaining > 0
			? calculateMinutesLength(order.quantity - (order.units_already_produced ?? 0), order.material)
			: 0;
		return order;
	});
	return orders;
}
