from fastapi import FastAPI, Depends
from pydantic import BaseModel

from factory import Order, factory_settings
from fastapi.middleware.cors import CORSMiddleware

from optimize import optimize_orders
from auth import check_user
from settings import settings


app = FastAPI(docs_url=None if settings.PROD else "/docs")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OptimizationInput(BaseModel):
    machines: list[factory_settings.machine_types_literal]
    orders: list[Order]
    max_perm_size: int


@app.post("/optimize")
async def root(
    optimization_input: OptimizationInput,
    dependencies=Depends(check_user),
):
    machines, orders, max_perm_size = (
        optimization_input.machines,
        optimization_input.orders,
        optimization_input.max_perm_size,
    )
    opt = optimize_orders(machines, orders, max_perm_size)
    return {k: v.items for k, v in opt.factory.machines.items()}
    # return {"machines": machines, "orders": orders}
