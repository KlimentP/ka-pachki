from __future__ import annotations
from dataclasses import field, dataclass
from datetime import datetime, timedelta
from typing import Literal
from uuid import uuid4


@dataclass
class Employee:
    id: str
    name: str
    machine: Literal["butter", "labels", "embossed_lids"]


@dataclass
class Order:
    order_id: str
    color_scheme: list[str]
    material: str
    minutes_length: int
    deadline: datetime
    days_remaining: timedelta = field(init=False)

    def __repr__(self) -> str:
        return f"Order {self.order_id} with {self.color_scheme}"

    def __post_init__(self):
        self.days_remaining = datetime.now() - self.deadline
        self.color_scheme = [
            x if x != "P Custom" else uuid4() for x in self.color_scheme
        ]

    def compute_switch_difference(self, other_order: Order):
        return len(set(self.color_scheme) - set(other_order.color_scheme)) * 20


@dataclass
class Machine:
    orders: list[Order]
    operating_employees: list[Employee]
    acceptable_materials: list[str]
    available_minutes: int = 8 * 60
    tolerance: float = 15
    switch_cost: int = 0

    def add_order(self, order: Order):
        if order.material not in self.acceptable_materials:
            raise ValueError("Order material does not match machine material")
        if order.hours_length > self.available_hours + self.tolerance:
            raise ValueError("Order too large for machine")
        self.orders.append(order)
        color_scheme_difference = order.compute_switch_difference(self.orders[-1])
        self.switch_cost += color_scheme_difference
        self.available_hours -= order.hours_length


def main():
    orders: list[Order] = []
    specific_materials = ["butter", "labels", "embossed_lids"]
    employees = {
        "Nasko": Employee("1", "Ivan", "labels"),
        "Ivan": Employee("2", "Nasko", "butter"),
        "Dragan": Employee("3", "Dragan", "embossed_lids"),
    }

    machines = {
        "butter": Machine([], ["lids", "butter"]),
        "labels": Machine([], ["lids", "labels"]),
        "embossed_lids": Machine([], ["lids", "embossed_lids"]),
    }

    # deterimine urgent orders
    urgent_orders = [
        x for x in orders if x.minutes_length / (60 * 8) - x.days_remaining <= 2
    ]

    # assign urgent orders
    for order in urgent_orders:
        # first send to specific employees (this should handle machines as well)
        if order.employee in employees:
            machines[order.employee.machine].add_order(order)
            urgent_orders.remove(order)
            break
        # then send to specific machines
        if order.material in specific_materials:
            machines[order.material].add_order(order)
            urgent_orders.remove(order)
            break
    # the rest of the urgent orders we will try to bundle together with non-urgent

    else:
        raise ValueError("No machine available for order")
