from itertools import permutations
from functools import partial

from multiprocessing import Pool
from factory import Order, factory_settings


# TODO think about this combo of material and employee
def conditional_perm(
    p: list[Order], specific_materials=factory_settings.material_types # TODO change back to specific types
) -> bool:  # sourcery skip: use-named-expression
    sum_mins = sum(x.minutes_length for x in p)

    if (
        sum_mins < factory_settings.min_run_time
        or sum_mins > factory_settings.available_lid_time
    ):
        return False
    # employees = [x.employee for x in p if x is not None]
    # if employees:
    #     employee_materials = {
    #         x.employee.machine for x in p if x.employee.machine in specific_materials
    #  # type: ignore
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


def get_all_perms(orders: list[Order], lengths: list[int], parallel: bool = True):
    perms = []
    if parallel:
        with Pool() as pool:
            res = pool.map(partial(get_permutations, orders), lengths)
            perms = [x for y in res for x in y]  # type: ignore
    else:
        for length in lengths:
            perms += get_permutations(orders, length)  # type: ignore
    return perms
