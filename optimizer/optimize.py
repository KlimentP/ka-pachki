from itertools import permutations

from factory import (
    Employee,
    FactorySettings,
    Machine,
    Order,
    Factory,
    Bundle,
    load_sample_orders,
    factory_settings,
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
            print(self.factory.status)
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
        print(self.factory.status)


class OptimizerUtils:
    def __init__(self, factory_settings: FactorySettings = factory_settings):
        self.factory_settings = factory_settings

    def narrow_down_orders(self, orders: list[Order]) -> list[Order]:
        # skip already completed:
        outstanding = [x for x in orders if x.status != "completed"]
        butters = [x for x in outstanding if x.material == "butter"]
        butters_duration = sum(x.minutes_length for x in butters)
        # skip butter orders if they are less than 350 minutes
        # and there are no urgent butter orders:
        if (
            butters_duration
            < self.factory_settings.available_butter_time
            - 2 * self.factory_settings.tolerance
            and not any(x.urgent for x in butters)
        ):
            return [x for x in orders if x.material != "butter"]
        return orders

    def get_threshold_duration(self, item: Bundle | Order):
        thresholds = {
            "butter": self.factory_settings.available_butter_time,
            "default": self.factory_settings.available_lid_time,
        }
        return thresholds.get(item.material, thresholds["default"])

    def break_down_big_orders(self, orders: list[Order]) -> list[Order]:
        # break down orders that are longer than the respective threshold:
        big_orders = [
            x for x in orders if x.minutes_length > self.get_threshold_duration(x)
        ]
        for order in big_orders:
            theshold = self.get_threshold_duration(order)
            order_count = order.minutes_length // theshold + 1
            remainder = order.minutes_length % theshold
            new_orders = [order.copy() for _ in range(order_count)]
            for i, new_order in enumerate(new_orders):
                new_order.id = f"{order.id}_{i}"
                new_order.minutes_length = theshold
            if remainder:
                new_orders[-1].minutes_length = remainder
            orders.remove(order)
            orders.extend(new_orders)
        return orders

    def sort_perms_by_machine(
        self,
        perms: list[list[Order]],
        machines: list[Machine],
        urgent_orders: list[Order] | None = None,
        max_perm_size: int = 4,
    ) -> dict[str, list[list[Order]]]:
        """
        This function sorts permutations of orders by machine.

        Args:
            perms: A list of lists of Order objects representing different permutations of orders.
            machines: A list of Machine objects.
            urgent_orders: A list of Order objects representing urgent orders.
            max_perm_size: The maximum size of a permutation.

        Returns:
            A dictionary where keys are machine names and values are lists of permutations of orders sorted by machine.
        """
        perms_by_machine = {x.name: [] for x in machines} # type: ignore
        urgent_orders = urgent_orders or []

        for machine in machines:
            if urgent_for_machine := self.get_urgent_orders_for_machine(
                machine, urgent_orders
            ):
                perms_by_machine[machine.name] = self.get_perms_for_machine(
                    perms, urgent_for_machine, max_perm_size
                )
            else:
                perms_by_machine[
                    machine.name
                ] = self.get_perms_for_machine_without_urgent(perms, machine)

        return perms_by_machine

    def get_urgent_orders_for_machine(
        self, machine: Machine, urgent_orders: list[Order]
    ) -> list[Order]:
        return [x for x in urgent_orders if x.material in machine.urgent_materials]

    def get_perms_for_machine(self, perms, urgent_for_machine, max_perm_size):
        if len(urgent_for_machine) == max_perm_size:
            return [urgent_for_machine]
        return [x for x in perms if all(y in x for y in urgent_for_machine)]

    def get_perms_for_machine_without_urgent(self, perms, machine):
        perms_for_machine = []
        for perm in perms:
            for order in perm:
                if (
                    order.material == "lid"
                    or order.material in machine.acceptable_materials
                ):
                    perms_for_machine.append(perm)
                    break
        return perms_for_machine

    def bundle_orders(self, orders: list[Order]) -> list[Order]:
        bundle_options = []
        # get unique combos of material + color scheme:
        for o in orders:
            prop = (o.material, set(o.computed_color_scheme))
            if prop not in bundle_options:
                bundle_options.append(prop)
        bundles = []
        for bundle_option in bundle_options:
            # bundle orders with same material and color scheme,
            # but less than threhold minutes because they would.or take who day anyways:
            temp_b = []
            for x in orders:
                if x.material == bundle_option[0] and set(
                    x.computed_color_scheme
                ) == set(bundle_option[1]):
                    if x.minutes_length >= self.get_threshold_duration(x):
                        bundles.append([x])
                        continue
                    temp_b.append(x)
            if temp_b:
                bundles.append(temp_b)
        # return standalone orders or bundles:
        return [x[0] if len(x) == 1 else Bundle(x) for x in bundles]


def optimize_orders(
    machine_employees: list[str],
    orders: list[Order],
    max_perm_size=4,
    optimizer_utils: OptimizerUtils = OptimizerUtils(),
    factory_settings: FactorySettings = factory_settings,
):
    
    machines = []
    for name in [x.name for x in machine_employees]:
        if name not in factory_settings.machine_types:
            raise ValueError(f"Invalid {name}")
        machines.append(
            Machine(
                name,
                [],
                factory_settings.machine_material_pairs[name]["acceptable_materials"],
                factory_settings.machine_material_pairs[name]["urgent_materials"],
            )
        )

    lengths = list(range(1, max_perm_size + 1))

    employees = [
        Employee("1", "Bobi",),
        Employee("2", "Sasho",),
        Employee("3", "Valter", ),
    ]
    filtered_orders = optimizer_utils.narrow_down_orders(orders)
    brokendown_orders = optimizer_utils.break_down_big_orders(filtered_orders.copy())
    bundles = optimizer_utils.bundle_orders(brokendown_orders)
    perms = get_all_perms(bundles, lengths, parallel=True)
    perm_by_machine = optimizer_utils.sort_perms_by_machine(perms, machines)
    # Define the batch size for permutations of length 6

    factory = Factory({m.name: m for m in machines})

    opt = PermOptimizer(factory, perm_by_machine)
    opt.fit_perms_factory()
    return opt
    # return {
    #     "orders": opt.factory.scheduled_orders,
    #     "status": opt.factory.status,
    # }
