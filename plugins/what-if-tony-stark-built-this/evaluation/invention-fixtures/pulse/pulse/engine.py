from .recipe import expand


def analyze(program):
    values = list(expand(program))
    if not values:
        return dict(count=0, sum=0, first=None, last=None, minimum=None, maximum=None, drawdown=0, rise=0)
    peak = values[0]
    drawdown = 0
    rise = best = 1
    for old, value in zip(values, values[1:]):
        peak = max(peak, value)
        drawdown = max(drawdown, peak-value)
        rise = rise+1 if value > old else 1
        best = max(best, rise)
    return dict(count=len(values), sum=sum(values), first=values[0], last=values[-1], minimum=min(values),
                maximum=max(values), drawdown=drawdown, rise=best)
