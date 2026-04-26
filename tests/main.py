from typing import Annotated, Optional

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/text")
async def get_text():
    return "Hello World"


@app.get("/path/{item_id}")
async def get_id(item_id):
    return item_id


@app.get("/path/str/{item_id}")
async def get_str_id(item_id: str):
    return item_id


@app.get("/path/int/{item_id}")
async def get_int_id(item_id: int):
    return item_id


@app.get("/path/float/{item_id}")
async def get_float_id(item_id: float):
    return item_id


@app.get("/path/bool/{item_id}")
async def get_bool_id(item_id: bool):
    return item_id


@app.get("/path/param/{item_id}")
async def get_path_param_id(item_id: str = Path()):
    return item_id


@app.get("/path/param-minlength/{item_id}")
async def get_path_param_min_length(item_id: Annotated[str, Path(min_length=3)]):
    return item_id


@app.get("/path/param-maxlength/{item_id}")
async def get_path_param_max_length(item_id: Annotated[str, Path(max_length=3)]):
    return item_id


@app.get("/path/param-min_maxlength/{item_id}")
async def get_path_param_min_max_length(
    item_id: Annotated[str, Path(min_length=2, max_length=3)],
):
    return item_id


@app.get("/path/param-gt/{item_id}")
async def get_path_param_gt(item_id: Annotated[float, Path(gt=3)]):
    return item_id


@app.get("/path/param-gt0/{item_id}")
async def get_path_param_gt0(item_id: Annotated[float, Path(gt=0)]):
    return item_id


@app.get("/path/param-ge/{item_id}")
async def get_path_param_ge(item_id: Annotated[float, Path(ge=3)]):
    return item_id


@app.get("/path/param-lt/{item_id}")
async def get_path_param_lt(item_id: Annotated[float, Path(lt=3)]):
    return item_id


@app.get("/path/param-lt0/{item_id}")
async def get_path_param_lt0(item_id: Annotated[float, Path(lt=0)]):
    return item_id


@app.get("/path/param-le/{item_id}")
async def get_path_param_le(item_id: Annotated[float, Path(le=3)]):
    return item_id


@app.get("/path/param-lt-gt/{item_id}")
async def get_path_param_lt_gt(item_id: Annotated[float, Path(gt=1, lt=3)]):
    return item_id


@app.get("/path/param-le-ge/{item_id}")
async def get_path_param_le_ge(item_id: Annotated[float, Path(ge=1, le=3)]):
    return item_id


@app.get("/path/param-lt-int/{item_id}")
async def get_path_param_lt_int(item_id: Annotated[int, Path(lt=3)]):
    return item_id


@app.get("/path/param-gt-int/{item_id}")
async def get_path_param_gt_int(item_id: Annotated[int, Path(gt=3)]):
    return item_id


@app.get("/path/param-le-int/{item_id}")
async def get_path_param_le_int(item_id: Annotated[int, Path(le=3)]):
    return item_id


@app.get("/path/param-ge-int/{item_id}")
async def get_path_param_ge_int(item_id: Annotated[int, Path(ge=3)]):
    return item_id


@app.get("/path/param-lt-gt-int/{item_id}")
async def get_path_param_lt_gt_int(item_id: Annotated[int, Path(gt=1, lt=3)]):
    return item_id


@app.get("/path/param-le-ge-int/{item_id}")
async def get_path_param_le_ge_int(item_id: Annotated[int, Path(ge=1, le=3)]):
    return item_id


@app.get("/query")
async def get_query(query: str):
    return f"foo bar {query}"


@app.get("/query/optional")
async def get_query_optional(query: Optional[str] = None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int")
async def get_query_int(query: int):
    return f"foo bar {query}"


@app.get("/query/int/optional")
async def get_query_int_optional(query: Optional[int] = None):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/int/default")
async def get_query_int_default(query: int = 10):
    return f"foo bar {query}"


@app.get("/query/param")
async def get_query_param(query: Optional[int] = Query(default=None)):
    if query is None:
        return "foo bar"
    return f"foo bar {query}"


@app.get("/query/param-required")
async def get_query_param_required(query: int = Query()):
    return f"foo bar {query}"


@app.get("/query/param-required/int")
async def get_query_param_required_int(query: int = Query()):
    return f"foo bar {query}"


@app.get("/query/frozenset/")
async def get_query_frozenset(query: frozenset[int] = Query()):
    return ",".join(str(x) for x in sorted(query))


@app.get("/query/list/")
async def get_query_list(device_ids: list[int] = Query()):
    return device_ids


@app.get("/query/list-default/")
async def get_query_list_default(device_ids: list[int] = Query(default=[])):
    return device_ids
