from __future__ import annotations

class PrintOrder:

    def __init__(self, color_scheme: list[str], material: str, hours_length: int, days_remaining: int, order_id: str):
        self.color_scheme = color_scheme
        self.material = material
        self.days_remaining = days_remaining
        self.order_id = order_id
        self.hours_length = hours_length
        self.urgent = days_remaining <= 2

    def compute_switch_difference(self, other_order: PrintOrder):
        return len(set(self.color_scheme) - set(other_order.color_scheme))

    def __repr__(self) -> str:
        return f"Order {self.order_id} with {self.color_scheme}"

class Machine:

    def __init__(self, orders: list[PrintOrder], available_hours: float, 
                 acceptable_materials: list[str], tolerance: float = 0.25):
        self.orders = orders
        self.available_hours = available_hours
        self.acceptable_materials = acceptable_materials
        self.tolerance = tolerance
        self.switch_cost = 0

    def add_order(self, order: PrintOrder):
        if order.material not in self.acceptable_materials:
            raise ValueError("Order material does not match machine material")
        if order.hours_length > self.available_hours + self.tolerance:
            raise ValueError("Order too large for machine")
        self.orders.append(order)
        color_scheme_difference = order.compute_switch_difference(self.orders[-1])
        self.switch_cost += color_scheme_difference
        self.available_hours -= order.hours_length


class OrderBundle:
    def __init__(self, orders: list[PrintOrder]):
        self.orders = orders
        self.total_hours = sum(order.hours_length for order in orders)

    def __repr__(self) -> str:
        return f"Bundle: {self.orders}"

class Optimizer:
    def __init__(self, orders: list[PrintOrder], machines: list[Machine]):
        self.orders = orders
        self.machines = machines
        self.bundles = [OrderBundle([order]) for order in orders]
    
    def aggregate_zero_cost_bundles(self):
        for i, bundle in enumerate(self.bundles):
            for j, other_bundle in enumerate(self.bundles):
                if i == j:
                    continue
                if bundle.orders[-1].compute_switch_difference(other_bundle.orders[-1]) > 0 or bundle.orders[-1].material != other_bundle.orders[-1].material:
                    continue
                # if bundle.total_hours + other_bundle.total_hours <= 8:
                bundle.orders.extend(other_bundle.orders)
                bundle.total_hours += other_bundle.total_hours
                self.bundles.pop(j)
                print(f'combining{str(bundle)}{str(other_bundle)}')
                self.aggregate_zero_cost_bundles()
                return
        return


labels = Machine([], 8, ["labels", "lids"])
butter = Machine([], 8, ["butter", "lids"])
embossed_lids = Machine([], 8, ["embossed_lids", "lids"])

orders = [
    PrintOrder(["red", "blue", "yellow"],  "butter", 1, 3, "1"),
    PrintOrder(["red", "blue", "yellow"],  "butter", 1, 3, "2"),
    PrintOrder(["red", "blue", "green"],  "lids", 1, 3, "3"),
    PrintOrder(["red", "blue", "green"],  "lids", 1, 3, "4"),
    PrintOrder(["red", "blue", "black"],  "lids", 1, 3, "5"),
]


opt = Optimizer(orders, [labels, butter, embossed_lids])
opt.aggregate_zero_cost_bundles()
print(opt.bundles)