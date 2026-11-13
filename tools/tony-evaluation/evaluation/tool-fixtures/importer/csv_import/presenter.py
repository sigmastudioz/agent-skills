def render(run):
    if run is None:
        return {"status": "missing", "processed": 0}
    return {"tenant": run["tenant"], "run_id": run["run_id"],
            "status": "complete" if run["next_row"] > 0 else "pending", "processed": run["next_row"]}
