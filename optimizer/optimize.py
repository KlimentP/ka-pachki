from itertools import permutations
import traceback

from factory import (
    Employee,
    Machine,
    Order,
    Factory,
    Bundle,
    mock_order,
    load_sample_orders,
    MACHINE_TYPES,
    MATERIAL_TYPES,
    OrderNotFittingException,
)
from permutations import get_all_perms


class PermOptimizer:
    def __init__(
        self,
        factory: Factory,
        perms: dict[str, list[list[Order]]],
        min_idle_time: float = 480,
    ):
        self.factory = factory
        self.perms = perms
        self.min_idle_time = min_idle_time
        self.optimized_idle_time = min_idle_time
        self.best_fit: dict | None = None

    @staticmethod
    def flatten_permutation(perm: list[list[Order | Bundle]]) -> list[Order]:
        orders_flat = []
        for p in perm:
            if isinstance(p, Bundle):
                orders_flat.extend(p.orders)
            else:
                orders_flat.append(p)
        return orders_flat

    def fit_perms_machine(
        self,
        machine_name: str,
    ):
        best_fit = {}
        machine: Machine = self.factory.machines[machine_name]
        min_idle_time = self.min_idle_time
        # factory.clear_orders()
        perms = self.perms[machine_name]
        print(f"checking {len(perms)} options for {machine_name}")
        for perm in perms:
            try:
                orders_flat = self.flatten_permutation(perm)
                self.factory.add_multiple_orders(orders_flat, machine_name)
            # if the perm doesn't fit, dont consider it for optimal solution:
            except (OrderNotFittingException, ValueError) as e:
                if isinstance(e, OrderNotFittingException):
                    continue
                raise Exception from e
            if (
                machine.idle_time < min_idle_time
                and machine.available_minutes >= -machine.tolerance
            ):
                min_idle_time = machine.idle_time
                best_fit = {
                    "idle_time": min_idle_time,
                    "perm": machine.items.copy(),
                }
            self.factory.clear_orders([machine_name])
        # re-add once we know the best perm
        if best_fit:
            self.factory.set_schedule(
                best_fit["perm"], best_fit["idle_time"], machine_name  # type: ignore
            )
            self.factory.update_status()
        else:
            print(f"No best fit found for {machine_name} ")

    def fit_perms_factory(self) -> None:
        min_idle_time: float = self.min_idle_time * len(self.factory.machines)
        best_fit = {}
        machine_perms = permutations(self.factory.machines)
        for mp in machine_perms:
            temp_fit = {}
            for machine in mp:
                self.fit_perms_machine(machine)
                temp_fit[machine] = {
                    "perm": self.factory.machines[machine].items,
                    "idle_time": self.factory.machines[machine].idle_time,
                }
            # self.factory.update_status()
            total_idle_time = sum(x["idle_time"] for x in temp_fit.values())
            if total_idle_time < min_idle_time:
                min_idle_time = total_idle_time
                self.optimized_idle_time = min_idle_time
                best_fit = temp_fit

            self.factory.clear_orders()
        # re-add once we know the best perm for each machine
        self.best_fit = best_fit
        for machine_name, fit in best_fit.items():
            self.factory.set_schedule(fit["perm"], fit["idle_time"], machine_name)
        self.factory.update_status()


def sort_perms_by_machine(
    perms: list[list[Order]],
    machine_names: list[str],
) -> dict[str, list[list[Order]]]:
    perms_by_machine: dict[str, list[list[Order]]] = {x: [] for x in machine_names}
    for perm in perms:
        for order in perm:
            if order.material == "lid":
                for m in machine_names:
                    perms_by_machine[m].append(perm)
                break
            if order.material in machine_names:
                perms_by_machine[order.material].append(perm)
                break

    return perms_by_machine


def narrow_down_orders(orders: list[Order]) -> list[Order]:
    # skip already completed:
    outstanding = [x for x in orders if x.status != "completed"]
    butters = [x for x in outstanding if x.material == "butter"]
    butters_duration = sum(x.minutes_length for x in butters)
    if butters_duration < 350:
        return [x for x in orders if x.material != "butter"]
    return orders


def break_down_big_orders(orders: list[Order]) -> list[Order]:
    # break down orders that are longer than 450 minutes:
    big_orders = [x for x in orders if x.minutes_length > 425]
    for order in big_orders:
        order_count = order.minutes_length // 425 + 1
        remainder = order.minutes_length % 425
        new_orders = [order.copy() for _ in range(order_count)]
        for i, new_order in enumerate(new_orders):
            new_order.id = f"{order.id}_{i}"
            new_order.minutes_length = 425
        if remainder:
            new_orders[-1].minutes_length = remainder
        orders.remove(order)
        orders.extend(new_orders)
    return orders


def bundle_orders(orders: list[Order]) -> list[Order]:
    bundle_options = []
    # get unique combos of material + color scheme:
    for o in orders:
        prop = (o.material, set(o.computed_color_scheme))
        if prop not in bundle_options:
            bundle_options.append(prop)
    bundles = []
    for bundle_option in bundle_options:
        # bundle orders with same material and color scheme,
        # but less than 425 minutes because they would.or take who day anyways:
        temp_b = []
        for x in orders:
            if x.material == bundle_option[0] and set(x.computed_color_scheme) == set(
                bundle_option[1]
            ):
                if x.minutes_length >= 425:
                    bundles.append([x])
                    continue
                temp_b.append(x)
        if temp_b:
            bundles.append(temp_b)
    # return standalone orders or bundles:
    return [x[0] if len(x) == 1 else Bundle(x) for x in bundles]


def optimize_orders(
    machine_names: list[str] | None = None,
    orders: list[Order] | None = None,
    max_perm_size=4,
):
    if machine_names is None:
        machine_names = MACHINE_TYPES
    lengths = [x for x in range(1, max_perm_size + 1)]
    if orders is None:
        employees = {
            "Bobi": Employee("1", "Bobi", "label"),
            "Sasho": Employee("2", "Sasho", "butter"),
            "Valter": Employee("3", "Valter", "embossed_lid"),
        }

        # orders = [mock_order(i, employees) for i in range(12)] #TODO drop once done
        orders = load_sample_orders()

    filtered_orders = narrow_down_orders(orders)
    brokendown_orders = break_down_big_orders(filtered_orders.copy())
    bundles = bundle_orders(brokendown_orders)
    perms = get_all_perms(bundles, lengths, parallel=True)
    perm_by_machine = sort_perms_by_machine(perms, machine_names)
    # Define the batch size for permutations of length 6
    machines_list = [Machine(x, [], ["lid", x]) for x in machine_names]
    machines = {x.name: x for x in machines_list}
    factory = Factory(machines)

    opt = PermOptimizer(factory, perm_by_machine)
    opt.fit_perms_factory()
    return opt
    # return {
    #     "orders": opt.factory.scheduled_orders,
    #     "status": opt.factory.status,
    # }


if __name__ == "__main__":
    orders, machine_names = None, None
    opt = optimize_orders()
    print("opt time", opt.optimized_idle_time)
    print("status", opt.factory.status)
    print("orders", opt.factory.scheduled_orders)
