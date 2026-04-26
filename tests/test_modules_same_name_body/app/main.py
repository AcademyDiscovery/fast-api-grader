from typing import Annotated

from fastapi import APIRouter, Body, FastAPI

app = FastAPI()

router_a = APIRouter(prefix="/a")
router_b = APIRouter(prefix="/b")


@router_a.post("/compute")
async def compute(a: Annotated[int, Body()], b: Annotated[str, Body()]):
    return {"a": a, "b": b}


@router_b.post("/compute/")
async def compute(a: Annotated[int, Body()], b: Annotated[str, Body()]):  # noqa: F811
    return {"a": a, "b": b}


app.include_router(router_a)
app.include_router(router_b)
