import time
from typing import Optional
from fastapi import FastAPI, Depends

from factory import Order
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


@app.post("/optimize")
async def root(
    machines: Optional[list[str]] = None,
    orders: Optional[list[Order]] = None,
    max_perm_size: Optional[int] = 3,
    dependencies=Depends(check_user),
):
    opt = optimize_orders(machines, orders, max_perm_size)
    return {k:v.items for k,v in opt.factory.machines.items()}
    # return {"machines": machines, "orders": orders}
