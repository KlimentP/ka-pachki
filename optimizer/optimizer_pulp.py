import pulp

from adhoc.optimizer import Machine, Order, OrderBundle, Factory, Employee, mock_order


class MachineWEmployee(Machine):
    employee: Employee


def main():
    prob = pulp.LpProblem("Printing_Scheduling", pulp.LpMinimize)
    orders: list[Order] = [mock_order() for _ in range(50)]
    specific_materials = ["butter", "labels", "embossed_lids"]
    machines = [Machine(x, [], ["lids", x]) for x in specific_materials]
    employees = [
        Employee("1", "Ivan", "labels"),
        Employee("2", "Nasko", "butter"),
        Employee("3", "Dragan", "embossed_lids"),
    ]
    factory = Factory(machines)
    order_machine_vars = pulp.LpVariable.dicts(
        "OrderMachine", (orders, machines), cat="Binary"
    )
    for order in orders:
        prob += (
            pulp.lpSum([order_machine_vars[order][machine] for machine in machines])
            == 1
        )
        # Add constraints for machine capabilities and employee-machine assignments
        for order in orders:
            for machine in machines:
                # Check if the machine can handle the order
                if order.material not in machine.acceptable_materials:
                    prob += order_machine_vars[order][machine] == 0

                # Check if the employee assigned to the machine can work on the design
                if (
                    order.employee is not None
                    and order.employee.machine != machine.name
                ):
                    prob += order_machine_vars[order][machine] == 0


