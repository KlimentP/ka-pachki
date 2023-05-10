from dataclasses import dataclass, field
import math
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
    ]

    material: Literal["butter", "labels", "embossed_lids", "lids"]
    minutes_length: int
    days_remaining: int
    urgent_bool: bool
    employee: Employee | None =  None 

    def __post_init__(self):
        self.color_scheme = [
            x if x != "P Custom" else uuid4() for x in self.color_scheme
        ]


@dataclass
class Machine:
    name: str
    orders: list[Order]
    # operating_employees: list[Employee]
    acceptable_materials: list[str]
    available_minutes_init = (8 * 60) - 40 - 30
    available_minutes: int = field(init=False)
    tolerance: float = 15
    switch_cost_minutes: int = 0
    full: bool = False
    idle_time: float = field(init=False)

    def __post_init__(self):
        self.available_minutes = self.available_minutes_init
        self.compute_idle_time()

    def check_full(self):
        self.full = self.available_minutes < self.tolerance

    def compute_idle_time(self):
        self.idle_time = self.available_minutes + self.switch_cost_minutes

    @staticmethod
    def compute_switch_difference(order1: Order, order2: Order) -> int:
        base = 20
        own, other = set(order1.color_scheme), set(order2.color_scheme)
        diff = (own | other) - (own & other)
        color_diff = len(diff) * 5
        if order1.material == order2.material:
            material_diff = 0
        elif "butter" in (order1.material, order2.material):
            material_diff = 120
        return base + color_diff + material_diff

    def add_order(self, order) -> None:
        self.orders.append(order)
        if len(self.orders) > 1:
            switch_difference = order.compute_switch_difference(self.orders[-2])
            self.switch_cost_minutes += switch_difference
        elif order.material == "butter":
            self.available_minutes -= 20
        self.available_minutes -= order.minutes_length

        self.compute_idle_time()
        self.check_full()

    def multiple_orders(self, orders: list[Order]):
        try:
            for order in orders:
                self.add_order(order)
            # if last order is butter, deduce further 30min:
            if orders[-1].material == "butter":
                self.available_minutes -= 30
        except ValueError as e:
            self.clear_orders()
            raise ValueError(e) from e

    def clear_orders(self) -> None:
        self.orders = []
        self.available_minutes = self.available_minutes_init
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
                print("from update factory status ", self.machines[m_temp].idle_time)
        self.status = {
            name: {
                "idle_time": machine.idle_time,
                "available_minutes": machine.available_minutes,
                "switch_cost_minutes": machine.switch_cost_minutes,
            }
            for name, machine in self.machines.items()
        }

    def check_if_order_fits(self, order: Order, m: Machine) -> bool:
        # if machine is full, do not accept further orders:
        if m.full:
            raise ValueError("Machine is full")
        # raise error if order is assigned to any of the machines:
        if order.material not in m.acceptable_materials:
            raise ValueError("Order material does not match machine material")
        if order.id in [x["order_id"] for x in self.scheduled_orders]:
            raise ValueError("Order already assigned")
        # if order.hours_length > self.available_hours + self.tolerance:
        #     raise ValueError("Order too large for machine")
        return True

    def add_order(self, order: Order, machine_name: str) -> None:
        m = self.machines[machine_name]
        self.check_if_order_fits(order, m)
        m.add_order(order)
        self.scheduled_orders.append(
            {"order_id": order.id, "machine_name": machine_name}
        )

    def add_multiple_orders(
        self,
        orders: list[Order],
        machine_name: str,
    ):
        try:
            for order in orders:
                self.add_order(order, machine_name)
        except ValueError as e:
            self.clear_orders(machine_names=[machine_name])
            raise ValueError(e)

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
            # "labels",
            "embossed_lids",
        ]
        + ["lids"] * 10
    )
    minutes_length = random.randrange(30, 180, 15)
    days_remaining = random.randint(1, 7)
    urgent = random.random() < 0.2
    # start_date = datetime.now().date()
    # end_date = date(2023, 5, 8)
    # delta_days = 7
    # deadline = start_date + timedelta(days=random.randint(1, delta_days))
    # deadline_str = deadline.strftime("%Y-%m-%d")

    employee = random.choice(employee_choices)
    return Order(
        order_id,
        color_scheme,
        material,  # type: ignore
        minutes_length,
        days_remaining,
        urgent,
        employee,  # type: ignore
    )


def convert_kg_to_m(kgs: int, material: str):
    return {
        "butter": (kgs * 3500) / 60,
        "lids": (kgs * 1500) / 28,
        "embossed_lids": (kgs * 1500) / 32,
        # "labels": (kgs * 1500) / 32,
    }[material]


def calculate_minutes_length(quantity_kgs: int, material: str):
    meters = convert_kg_to_m(quantity_kgs, material)
    roll_length = {
        "lids": {"length": 1500, "roll_duration": 35},
        "embossed_lids": {"length": 1500, "roll_duration": 35},
        # "labels": 10000,
        "butter": {"length": 3500, "roll_duration": 85},
    }
    runs = math.ceil(meters / roll_length[material]["length"])
    breaks = runs - 1
    return (breaks * 5) + (runs * roll_length[material]["roll_duration"])


def tt():
    o = (56, "lids")
    print(calculate_minutes_length(*o))
