from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from uuid import uuid4
import random


@dataclass
class Employee:
    id: str
    name: str
    machine: Literal["butter", "labels", "embossed_lids"]


@dataclass
class Order:
    id: int
    color_scheme: list[
        str
    ]  # 3 to 6 colors long one of the following: W	 Y	 P485	 C	 M	 Warm Red	 P288	 P375	 K	 Cool Grey	 Refl. Blue	 P Custom	 P361	 P2200	 Blue 072	 Cool Grey 5	 P2745	 Purple	 P1788	 P354	 P2727	 Cool Grey 4

    material: Literal["butter", "labels", "embossed_lids", "lids"]
    minutes_length: int  # between 30 and 960
    days_remaining: int
    employee: str | None = None  # usually none but sometimes on of Ivan, Nasko, Dragan

    def __post_init__(self):
        self.color_scheme = [
            x if x != "P Custom" else uuid4() for x in self.color_scheme
        ]

    def compute_switch_difference(self, other_order: Order):
        return len(set(self.color_scheme) - set(other_order.color_scheme)) * 20


@dataclass
class Machine:
    name: str
    orders: list[Order]
    # operating_employees: list[Employee]
    acceptable_materials: list[str]
    available_minutes: int = 8 * 60
    tolerance: float = 15
    switch_cost_minutes: int = 0
    full: bool = False
    idle_time: float = field(init=False)

    def __post_init__(self):
        self.compute_idle_time()

    def check_full(self):
        self.full = self.available_minutes < self.tolerance

    def compute_idle_time(self):
        self.idle_time = self.available_minutes + self.switch_cost_minutes

    def clear_orders(self):
        self.orders = []
        self.available_minutes = 8 * 60
        self.switch_cost_minutes = 0
        self.full = False
        self.compute_idle_time()


@dataclass
class Factory:
    machines: dict[str, Machine]
    least_busy_machine: Machine | None = None
    full_machines: list[Machine] = field(default_factory=list)
    scheduled_orders: list[dict] = field(default_factory=list)
    status: dict = field(default_factory=dict)

    def update_status(self, machine_names: list[str] | None = None) -> None:
        if machine_names is None:
            machine_names = list(self.machines.keys())
            for m_temp in machine_names:
                self.machines[m_temp].compute_idle_time()
        self.status = {
            name: {
                "idle_time": machine.idle_time,
                "available_minutes": machine.available_minutes,
                "switch_cost_minutes": machine.switch_cost_minutes,
            }
            for name, machine in self.machines.items()
        }

    def add_order(self, order: Order, machine_name: str) -> None:
        m = self.machines[machine_name]
        # if machine is full, do not accept further orders:
        if m.full:
            raise ValueError("Machine is full")
        # raise error if order is assigned to any of the machines:
        if order.id in [x["order_id"] for x in self.scheduled_orders]:
            raise ValueError("Order already assigned")
        if order.material not in m.acceptable_materials:
            raise ValueError("Order material does not match machine material")
        # if order.hours_length > self.available_hours + self.tolerance:
        #     raise ValueError("Order too large for machine")
        m.orders.append(order)
        self.scheduled_orders.append(
            {"order_id": order.id, "machine_name": machine_name}
        )
        if len(m.orders) > 1:
            color_scheme_difference = order.compute_switch_difference(m.orders[-2])
            m.switch_cost_minutes += color_scheme_difference
        m.available_minutes -= order.minutes_length
        m.check_full()

    def add_multiple_orders(
        self, orders: list[Order], machine_name: str, verbose: bool = False
    ):
        for order in orders:
            try:
                self.add_order(order, machine_name)
            except ValueError as e:
                if verbose:
                    print(f"Issue with {order.id} - {e}")
                self.clear_orders(machine_names=[machine_name])
        self.machines[machine_name].compute_idle_time()

    def clear_orders(
        self,
        machine_names: list[str] | None = None,
    ):
        if machine_names is None:
            machine_names = list(self.machines.keys())
        for m in self.machines:
            self.machines[m].clear_orders()
        self.scheduled_orders = [
            x for x in self.scheduled_orders if x["machine_name"] not in machine_names
        ]

    def __repr__(self) -> str:
        string = f"""Factory with {len(self.machines)} machines. """
        for m in self.machines.values():
            string += f"""{m.name}, {m.idle_time}: {m.available_minutes} time left, {m.switch_cost_minutes} switching with orders: {m.orders}. \n"""
        return string


def mock_order(order_id, employees: dict[str, Employee]):
    color_choices = [
        "P485",
        "Warm Red",
        "P288",
        "P375",
        "Cool Grey",
        "Refl. Blue",
        "P361",
        "P2200",
        "Blue 072",
        "Cool Grey 5",
        "P2745",
        "Purple",
        "P1788",
        "P354",
        "P2727",
        "Cool Grey 4",
    ] + ["P Custom"] * 5
    employee_choices = list(employees.values()) + [None] * 20
    # order_id = uuid4()
    color_scheme = (
        ["W"]
        + random.sample(
            [
                "Y",
                "C",
                "M",
                "K",
            ],
            2,
        )
        + random.sample(color_choices, random.randint(0, 3))
    )
    material = random.choice(
        [
            "butter",
            "labels",
            "embossed_lids",
        ]
        + ["lids"] * 10
    )
    minutes_length = random.randrange(30, 180, 15)
    days_remaining = random.randint(1, 7)
    # start_date = datetime.now().date()
    # end_date = date(2023, 5, 8)
    # delta_days = 7
    # deadline = start_date + timedelta(days=random.randint(1, delta_days))
    # deadline_str = deadline.strftime("%Y-%m-%d")

    employee = random.choice(employee_choices)
    return Order(
        order_id,
        color_scheme,
        material, # type: ignore
        minutes_length,
        days_remaining,
        employee, # type: ignore 
    )
