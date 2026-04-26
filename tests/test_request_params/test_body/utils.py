def get_body_model_name(openapi: dict, path: str) -> str:
    path_data = openapi["paths"][path]
    method_data = next(iter(path_data.values()))
    content = method_data["requestBody"]["content"]
    schema = next(iter(content.values()))["schema"]
    ref = schema["$ref"]
    return ref.split("/")[-1]
