from .model import Series
from .engine import first_overlap


def plan(request):
    lower, upper = request["lower"], request["upper"]
    if type(lower) is not int or type(upper) is not int or lower >= upper:
        raise ValueError("invalid query range")
    schedules = []
    seen = set()
    for item in request["schedules"]:
        name = item["id"]
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("invalid schedule ID")
        seen.add(name)
        schedules.append((name, Series(*(item[k] for k in ("start", "period", "duration", "count")))))
    schedules.sort(key=lambda pair: pair[0])
    rows = []
    for index, (left, a) in enumerate(schedules):
        for right, b in schedules[index + 1:]:
            at = first_overlap(a, b, lower, upper)
            if at is not None:
                rows.append({"left": left, "right": right, "at": at})
    return {"conflicts": sorted(rows, key=lambda row: (row["at"], row["left"], row["right"]))}
