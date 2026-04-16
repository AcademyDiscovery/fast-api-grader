# fast-api-grader

Automated grader for the FastAPI contribution course.
Mirrors the structure of [pandas-grader](https://github.com/AcademyDiscovery/pandas-grader)
and runs custom tests against student forks of the
[fastapi/fastapi](https://github.com/fastapi/fastapi) repository.

## Exercise — Fix `generate_unique_id` non-determinism

### The bug

`fastapi/utils.py` contains the helper that builds OpenAPI `operationId` strings:

```python
def generate_unique_id(route: "APIRoute") -> str:
    operation_id = f"{route.name}{route.path_format}"
    operation_id = re.sub(r"\W", "_", operation_id)
    assert route.methods
    operation_id = f"{operation_id}_{list(route.methods)[0].lower()}"  # ← bug
    return operation_id
```

`route.methods` is a Python `set`.  Sets have **no guaranteed iteration order**, so
`list(route.methods)[0]` may return a different HTTP method each time the process
starts (Python randomises hash seeds by default via `PYTHONHASHSEED`).  When a
route is registered with more than one method (e.g. `methods=["GET", "POST"]`),
the generated `operationId` can differ between runs, breaking OpenAPI schema
stability.

### The fix

Replace `list(route.methods)[0]` with `sorted(route.methods)[0]` so the
alphabetically first method is always chosen:

```python
operation_id = f"{operation_id}_{sorted(route.methods)[0].lower()}"
```

### How grading works

1. A student **forks** `fastapi/fastapi` and applies the fix above.
2. Their fork's CI calls this grader via `workflow_call`.
3. The grader:
   - installs the student's version of FastAPI with `pip install -e ./student-code`
   - checks out this repo to obtain `tests/test_fix.py`
   - runs the custom tests with pytest
   - posts the result as a PR comment (✅ or ❌)

### Calling the grader from a student fork

Add the following workflow file to the student's fastapi fork at
`.github/workflows/grade.yml`:

```yaml
on:
  pull_request:

jobs:
  grade:
    uses: AcademyDiscovery/fast-api-grader/.github/workflows/run-tests.yml@main
    secrets: inherit
```

## Repository structure

```
.
├── .github/
│   └── workflows/
│       └── run-tests.yml   # reusable grading workflow (workflow_call)
├── tests/
│   └── test_fix.py         # custom pytest tests run against the student's code
└── README.md
```
