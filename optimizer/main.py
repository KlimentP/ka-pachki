from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder

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
    dependencies=Depends(check_user),
):
    with open("orders.json", "w") as f:
        import json
        json.dump(jsonable_encoder(orders), f)
    return {"machines": machines, "orders": orders}
    # return optimize_orders(machine_names, orders)
