from dataclasses import dataclass


@dataclass(frozen=True)
class Series:
    start: int
    period: int
    duration: int
    count: int

    def __post_init__(self):
        if any(type(v) is not int for v in (self.start, self.period, self.duration, self.count)):
            raise ValueError("integer fields required")
        if self.period <= 0 or not 1 <= self.duration <= min(64, self.period) or self.count < 0:
            raise ValueError("invalid series")

    def occurrences(self, lower, upper, limit=10000):
        first = max(0, (lower - self.start - self.duration) // self.period + 1)
        emitted = 0
        for i in range(first, self.count):
            begin = self.start + i * self.period
            if begin >= upper:
                return
            emitted += 1
            if emitted > limit:
                raise ValueError("occurrence expansion limit")
            yield max(begin, lower), min(begin + self.duration, upper)
