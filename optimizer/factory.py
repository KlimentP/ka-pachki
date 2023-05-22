from dataclasses import dataclass, field
import json
from pydantic import BaseModel, Field, root_validator, BaseSettings
import math
from typing import Literal
from uuid import uuid4
import random
from typing import Protocol


@dataclass
class DownTime:
    name: str
    type: Literal["cleanup", "switch"]
    minutes_length: int

    def process(self, machine):
        machine.add_down_time(self)


class FactorySettings(BaseSettings):
    start_cleanup: DownTime = DownTime("Start", "cleanup", 30)
    butter_extra_start_cleanup: DownTime = DownTime("Butter Clean", "cleanup", 20)
    end_cleanup: DownTime = DownTime("End", "cleanup", 40)
    butter_switch = DownTime("Butter Clean", "cleanup", 30)
    total_time: int = 6 * 80
    tolerance: int = 15
    min_run_time: int = 240
    available_butter_time: int = (
        total_time
        - start_cleanup.minutes_length
        - butter_extra_start_cleanup.minutes_length
        - end_cleanup.minutes_length
        + tolerance
    )
    available_lid_time: int = (
        total_time
        - start_cleanup.minutes_length
        - end_cleanup.minutes_length
        + tolerance
    )
    machine_types_literal = Literal["butter", "label", "embossed_lid"]
    machine_types = machine_types_literal.__args__  # type: ignore
    material_types_literal = Literal[
        "butter", "label", "embossed_lid", "uv_butter", "lid"
    ]
    material_types = material_types_literal.__args__ # type: ignore
    specific_types = [x for x in material_types if x != "lid"] 
    base_switch: int = 20
    color_switch: int = 5
    lid_to_butter_switch: int = 120
    same_material_switch: int = 0


factory_settings = FactorySettings()


@dataclass
class Employee:
    id: str
    name: str
    # machine: factory_settings.machine_types_literal  # type: ignore


class Order(BaseModel):
    id: str
    type = "order"
    color_scheme: list[str]
    computed_color_scheme: list[str] | None
    design_name: str
    quantity: int
    units_already_produced: int
    deadline: str | None
    material: factory_settings.material_types_literal  # type: ignore
    minutes_length: int | None
    days_remaining: int = 7
    urgent: bool
    employee: str | None = None
    status: str  # TODO add enum

    class Config:
        arbitrary_types_allowed = True

    @root_validator()
    def format_color(cls, values):
        values["computed_color_scheme"] = [
            x if x != "P Custom" else uuid4() for x in values["color_scheme"]
        ]
        return values

    def process(self, machine):
        machine.add_order(self)

    def __repr__(self):
        return f"Order {self.id} of {self.material}, {self.minutes_length} min, {self.color_scheme}"


@dataclass
class Bundle:
    type = "bundle"
    orders: list[Order]
    minutes_length: int = Field(init=False)
    material: factory_settings.material_types_literal = Field(init=False)  # type: ignore

    def __post_init__(self):
        self.minutes_length = sum(x.minutes_length for x in self.orders)
        self.material = self.orders[0].material

    def process(self, machine):
        machine.multiple_orders(self.orders)


class Processable(Protocol):
    id: str | int
    minutes_length: int
    type: Literal["cleanup", "switch", "order", "bundle"]

    def process(self, machine) -> None:
        pass


@dataclass
class Machine:
    name: factory_settings.machine_types_literal  # type: ignore
    items: list[Order | DownTime]
    # operating_employees: list[Employee]
    acceptable_materials: list[factory_settings.machine_types_literal]  # type: ignore
    capacity_minutes: int = factory_settings.total_time
    tolerance: float = factory_settings.tolerance
    full: bool = False
    idle_time = capacity_minutes
    available_minutes = capacity_minutes

    def __post_init__(self):
        self.initialize_cleanups()

    def initialize_cleanups(self):
        self.add_down_time(factory_settings.start_cleanup, initial=True)
        self.add_down_time(factory_settings.end_cleanup, initial=True)

    def deduct_item_minutes(self, item):
        self.available_minutes -= item.minutes_length
        if item.type == "order":
            self.idle_time -= item.minutes_length
        self.check_full()

    def check_full(self):
        self.full = self.available_minutes < self.tolerance

    def add_down_time(self, downtime, initial=False) -> None:
        if initial:
            self.items.append(downtime)
        else:
            self.items[-1:-1] = [downtime]
        self.deduct_item_minutes(downtime)

    @staticmethod
    def compute_switch_difference(
        order1: Order,
        order2: Order,
        switch_settings: FactorySettings = factory_settings,
    ) -> int:
        own, other = set(order1.color_scheme), set(order2.color_scheme)
        diff = (own | other) - (own & other)
        color_diff = len(diff) * switch_settings.color_switch
        material_diff = switch_settings.same_material_switch

        # this handles butter and uv_butter:
        if any("butter" in x for x in (order1.material, order2.material)):
            material_diff = switch_settings.lid_to_butter_switch
        return switch_settings.base_switch + color_diff + material_diff

    def add_item(self, item: Processable) -> None:
        item.process(self)

    def add_order(self, order) -> None:
        if len(self.items) > 2:
            if self.items[-2].type == "switch":
                raise ValueError("Cannot add order after switch")
            switch_difference = self.compute_switch_difference(self.items[-2], order)  # type: ignore
            switch = DownTime("Switch", "switch", switch_difference)
            # inserting first switch, then order, always before the cleanup:
            self.add_item(switch)  # type: ignore
        elif order.material == "butter":
            self.add_item(factory_settings.butter_extra_start_cleanup)  # type: ignore
        self.items[-1:-1] = [order]
        self.deduct_item_minutes(order)

    def multiple_orders(self, orders: list[Order]):
        try:
            for order in orders:
                self.add_order(order)
            # if last order is butter, deduce further 30min:
            if orders[-1].material == "butter":
                self.add_down_time(factory_settings.butter_switch)
        except ValueError as e:
            self.clear_orders()
            raise ValueError(e) from e

    def clear_orders(self) -> None:
        # set full to false, reset idle time and clear items:
        self.full = False
        self.idle_time = self.capacity_minutes
        self.available_minutes = self.capacity_minutes
        self.items = []
        # start again with the start and end downtime:
        self.initialize_cleanups()


class OrderNotFittingException(Exception):
    pass


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
            # for m_temp in machine_names:
        self.status = {
            name: {
                "idle_time": machine.idle_time,
                "full": machine.full,
            }
            for name, machine in self.machines.items()
        }

    def check_if_order_fits(self, order: Order, m: Machine) -> None:
        # if machine is full, do not accept further orders:
        if m.full:
            raise OrderNotFittingException("Machine is full")
        # raise error if order is assigned to any of the machines:
        if order.material not in m.acceptable_materials:
            raise OrderNotFittingException(
                "Order material does not match machine material"
            )
        if order.id in [x["order_id"] for x in self.scheduled_orders]:
            raise OrderNotFittingException("Order already assigned")

    def add_order(self, order: Order, machine_name: str) -> None:
        m = self.machines[machine_name]
        self.check_if_order_fits(order, m)
        m.add_order(order)
        self.scheduled_orders.append(
            {"order_id": order.id, "machine_name": machine_name}
        )

    def set_schedule(
        self,
        items: list[Processable],
        idle_time: int,
        machine_name: str,
    ):
        m = self.machines[machine_name]
        m.clear_orders()
        m.idle_time = idle_time
        m.items = items  # type: ignore
        self.scheduled_orders.extend(
            [
                {"order_id": x.id, "machine_name": machine_name}
                for x in items
                if x.type == "order"
            ]
        )
        self.update_status()

    def add_multiple_orders(
        self,
        items: list[Order],
        machine_name: str,
    ):
        try:
            for item in items:
                if item.type == "order":
                    self.add_order(item, machine_name)
        except OrderNotFittingException as e:
            self.clear_orders(machine_names=[machine_name])
            raise OrderNotFittingException(e) from e

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
            string += f"""{m.name}, {m.idle_time}: {m.available_minutes} time left, switching with orders: {m.items}. \n"""
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
            # "label",
            "embossed_lid",
        ]
        + ["lid"] * 10
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
        id=order_id,
        color_scheme=color_scheme,
        material=material,  # type: ignore
        minutes_length=minutes_length,
        days_remaining=days_remaining,
        urgent=urgent,
        employee=employee,  # type: ignore
    )


def convert_kg_to_m(kgs: int, material: str):
    return {
        "butter": (kgs * 3500) / 60,
        "lid": (kgs * 1500) / 28,
        "embossed_lid": (kgs * 1500) / 32,
        # "label": (kgs * 1500) / 32,
    }[material]


def calculate_minutes_length(quantity_kgs: int, material: str):
    meters = convert_kg_to_m(quantity_kgs, material)
    roll_length = {
        "lid": {"length": 1500, "roll_duration": 35},
        "embossed_lid": {"length": 1500, "roll_duration": 35},
        # "label": 10000,
        "butter": {"length": 3500, "roll_duration": 85},
    }
    runs = math.ceil(meters / roll_length[material]["length"])
    breaks = runs - 1
    return (breaks * 5) + (runs * roll_length[material]["roll_duration"])


def load_sample_orders():
    with open("orders.json", "r") as f:
        orders = json.load(f)
        return [Order(**order) for order in orders]
