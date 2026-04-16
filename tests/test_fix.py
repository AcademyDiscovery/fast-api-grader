import ast
import inspect


def _get_utils_source() -> str:
    """Return the source code of fastapi/utils.py from the installed package."""
    import fastapi.utils

    return inspect.getsource(fastapi.utils)


def _find_function(source: str, func_name: str):
    """Return the AST FunctionDef node for func_name, or None."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return node
    return None


def _function_source_lines(source: str, func_name: str) -> list[str]:
    """Return the raw source lines for func_name."""
    tree = ast.parse(source)
    lines = source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return lines[node.lineno - 1 : node.end_lineno]
    return []


def test_generate_unique_id_function_exists():
    """generate_unique_id must exist in fastapi/utils.py."""
    source = _get_utils_source()
    node = _find_function(source, "generate_unique_id")
    assert node is not None, "generate_unique_id not found in fastapi/utils.py"


def test_generate_unique_id_uses_sorted():
    """generate_unique_id must use sorted(route.methods) for deterministic output."""
    source = _get_utils_source()
    func_lines = _function_source_lines(source, "generate_unique_id")
    assert func_lines, "generate_unique_id not found in fastapi/utils.py"
    func_text = "\n".join(func_lines)

    assert "sorted(route.methods)" in func_text, (
        "generate_unique_id must use sorted(route.methods) to guarantee "
        "a deterministic operation ID when a route has multiple HTTP methods. "
        "route.methods is a set, and sets do not have a guaranteed iteration order."
    )


def test_generate_unique_id_list_not_used():
    """generate_unique_id must not use list(route.methods)[0] (non-deterministic)."""
    source = _get_utils_source()
    func_lines = _function_source_lines(source, "generate_unique_id")
    assert func_lines, "generate_unique_id not found in fastapi/utils.py"
    func_text = "\n".join(func_lines)

    assert "list(route.methods)[0]" not in func_text, (
        "Found list(route.methods)[0] in generate_unique_id — "
        "this is non-deterministic because route.methods is a set. "
        "Replace it with sorted(route.methods)[0]."
    )


def test_generate_unique_id_alphabetical_method_order():
    """generate_unique_id must pick the alphabetically first HTTP method."""
    from fastapi import FastAPI
    from fastapi.routing import APIRoute
    from fastapi.utils import generate_unique_id

    app = FastAPI()

    @app.api_route("/items", methods=["POST", "GET"])
    def list_items():
        return []

    routes = [
        r for r in app.routes if isinstance(r, APIRoute) and r.path == "/items"
    ]
    assert routes, "Test route /items not found in app"
    route = routes[0]

    result = generate_unique_id(route)
    assert result.endswith("_get"), (
        f"generate_unique_id should use the alphabetically first method ('get') "
        f"but returned '{result}'. "
        f"When route.methods is {{'POST', 'GET'}}, sorted() gives ['GET', 'POST'], "
        f"so the operation ID must end with '_get'."
    )


def test_generate_unique_id_is_consistent():
    """generate_unique_id must return the same value on every call for the same route."""
    from fastapi import FastAPI
    from fastapi.routing import APIRoute
    from fastapi.utils import generate_unique_id

    app = FastAPI()

    @app.api_route("/check", methods=["PUT", "GET", "DELETE"])
    def check_endpoint():
        return {}

    routes = [
        r for r in app.routes if isinstance(r, APIRoute) and r.path == "/check"
    ]
    assert routes, "Test route /check not found in app"
    route = routes[0]

    results = [generate_unique_id(route) for _ in range(20)]
    unique = set(results)
    assert len(unique) == 1, (
        f"generate_unique_id returned different values across calls: {unique}. "
        "The function must be deterministic."
    )

    # With sorted(), the first method alphabetically among delete, get, put is 'delete'
    assert results[0].endswith("_delete"), (
        f"Expected the operation ID to end with '_delete' (alphabetically first of "
        f"delete, get, put) but got '{results[0]}'"
    )
