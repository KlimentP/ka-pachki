from datetime import datetime
from itertools import permutations
from functools import partial

from multiprocessing import Pool

# import sys
# sys.path.append('/home/kliment/ka-pachki/adhoc/optimizer.py')
from optimizer import Employee, Machine, Order, Factory, mock_order



#TODO think about this combo of material and employee
def conditional_perm(
    p: list[Order], specific_materials=("labels", "butter", "embossed_lids")
) -> bool:  # sourcery skip: use-named-expression
    sum_mins = sum(x.minutes_length for x in p)

    if sum_mins < 400 or sum_mins > 495:
        return False
    # employees = [x.employee for x in p if x is not None]
    # if employees:
    #     employee_materials = {
    #         x.employee.machine for x in p if x.employee.machine in specific_materials # type: ignore
    #     }  

    if len(p) == 1:
        return True
    spec_materials = {o.material for o in p if o.material in specific_materials}
    return len(spec_materials) <= 1


def temp(p: list[Order]) -> list[Order] | None:
    return p if conditional_perm(p) else None


# Define a function to generate permutations of a given length
def get_permutations(orders: list[Order], length: int) -> list[list[Order]]:
    # Generate all permutations of the given length for the list of items
    perms = permutations(orders, length)
    return [x for x in perms if conditional_perm(x)]  # type: ignore


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

    def fit_perms_machine(
        self,
        machine_name: str,
    ):
        best_fit = {}
        machine = self.factory.machines[machine_name]
        min_idle_time = self.min_idle_time
        # factory.clear_orders()
        perms = self.perms[machine_name]
        print(f"checking {len(perms)} options for {machine_name}")
        for perm in perms:
            try:
                self.factory.add_multiple_orders(perm, machine_name)
            except Exception:
                continue
            if machine.idle_time < min_idle_time:
                min_idle_time = machine.idle_time
                best_fit = {
                    "idle_time": min_idle_time,
                    "switch_cost": machine.switch_cost_minutes,
                    "available_minutes": machine.available_minutes,
                    "perm": perm,
                }

            self.factory.clear_orders([machine_name])
        # re-add once we know the best perm
        if best_fit:
            self.factory.add_multiple_orders(
                best_fit["perm"], machine_name  # type: ignore
            )
            self.factory.update_status()
        else:
            print(f"No best fit found for {machine_name} ")
        print(machine.idle_time)

    def fit_perms_factory(self) -> None:
        min_idle_time: float = self.min_idle_time * len(self.factory.machines)
        best_fit = {}
        machine_perms = permutations(self.factory.machines)
        for mp in machine_perms:
            temp_fit = {}
            for machine in mp:
                self.fit_perms_machine(machine)
                temp_fit[machine] = self.factory.machines[machine].orders
            self.factory.update_status()
            total_idle_time = sum(x.idle_time for x in self.factory.machines.values())
            print(mp, total_idle_time)
            if total_idle_time < min_idle_time:
                min_idle_time = total_idle_time
                self.optimized_idle_time = min_idle_time
                best_fit = temp_fit
                print(mp, best_fit)
            self.factory.clear_orders()
        # re-add once we know the best perm for each machine
        self.best_fit = best_fit
        for machine, orders in best_fit.items():
            self.factory.add_multiple_orders(orders, machine)
        self.factory.update_status()


def get_all_perms(orders: list[Order], lengths: list[int], parallel: bool = True):
    perms = []
    if parallel:
        with Pool() as pool:
            res = pool.map(partial(get_permutations, orders), lengths)
            perms = [x for y in res for x in y]  # type: ignore
    else:
        for length in lengths:
            print(datetime.now(), length)
            perms += get_permutations(orders, length)  # type: ignore
    return perms


def sort_perms_by_machine(
    perms: list[list[Order]],
    machine_names: list[str],
) -> dict[str, list[list[Order]]]:
    perms_by_machine: dict[str, list[list[Order]]] = {x: [] for x in machine_names}
    for perm in perms:
        for order in perm:
            if order.material == "lids":
                for m in machine_names:
                    perms_by_machine[m].append(perm)
                break
            if order.material in machine_names:
                perms_by_machine[order.material].append(perm)
                break

    return perms_by_machine


def narrow_down_orders(orders: list[Order]) -> list[Order]:
    butters = [x for x in orders if x.material == "butter"]
    butters_duration = sum(x.minutes_length for x in butters)
    if butters_duration < 350:
        return [x for x in orders if x.material != "butter"]
    return orders


def main() -> PermOptimizer:
    # Define the lengths of permutations to generate
    lengths = [1, 2, 3, 4, 5,]
    employees = {
        "Bobi": Employee("1", "Bobi", "labels"),
        "Sasho": Employee("2", "Sasho", "butter"),
        "Valter": Employee("3", "Valter", "embossed_lids"),
    }

    orders = [mock_order(i, employees) for i in range(12)]
    filtered_orders = narrow_down_orders(orders)

    perms = get_all_perms(filtered_orders, lengths, parallel=True)
    machine_names = ["butter", "labels", "embossed_lids"]
    perm_by_machine = sort_perms_by_machine(perms, machine_names)
    # Define the batch size for permutations of length 6
    machines_list = [Machine(x, [], ["lids", x]) for x in machine_names]
    machines = {x.name: x for x in machines_list}
    factory = Factory(machines)

    opt = PermOptimizer(factory, perm_by_machine)
    opt.fit_perms_factory()
    return opt


# if __name__ == "__main__":
#     opt = main()
#     # print(opt.best_fit)
#     print("opt time", opt.optimized_idle_time)
#     print("status", opt.factory.status)
#     print("orders", opt.factory.scheduled_orders)
