from fastapi import FastAPI, Depends

from permutations import optimize_orders
from auth import check_user
from settings import settings


app = FastAPI(docs_url=None if settings.PROD else "/docs")


@app.get("/optimize")
async def root(dependencies=Depends(check_user)):
    return optimize_orders()
