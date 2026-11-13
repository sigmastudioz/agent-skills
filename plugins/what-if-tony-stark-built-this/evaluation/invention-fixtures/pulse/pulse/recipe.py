def validate(node, depth=0):
    if depth > 64 or not isinstance(node, dict):
        raise ValueError("invalid program")
    keys = set(node)
    if keys == {"values"}:
        if not isinstance(node["values"], list) or any(type(v) is not int for v in node["values"]):
            raise ValueError("invalid values")
    elif keys == {"concat"}:
        if not isinstance(node["concat"], list):
            raise ValueError("invalid concat")
        for child in node["concat"]:
            validate(child, depth+1)
    elif keys == {"repeat", "body"}:
        if type(node["repeat"]) is not int or node["repeat"] < 0:
            raise ValueError("invalid repeat")
        validate(node["body"], depth+1)
    else:
        raise ValueError("invalid program keys")


def expand(program, limit=10000):
    validate(program)
    emitted = 0

    def visit(node):
        nonlocal emitted
        if "values" in node:
            for value in node["values"]:
                emitted += 1
                if emitted > limit:
                    raise ValueError("sample expansion limit")
                yield value
        elif "concat" in node:
            for child in node["concat"]:
                yield from visit(child)
        else:
            for _ in range(node["repeat"]):
                yield from visit(node["body"])

    yield from visit(program)
