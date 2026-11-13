def first_overlap(a, b, lower, upper):
    if type(lower) is not int or type(upper) is not int or lower >= upper:
        raise ValueError("invalid query range")
    left = list(a.occurrences(lower, upper))
    right = list(b.occurrences(lower, upper))
    best = None
    for x, xe in left:
        for y, ye in right:
            at = max(x, y)
            if at < min(xe, ye) and (best is None or at < best):
                best = at
    return best
