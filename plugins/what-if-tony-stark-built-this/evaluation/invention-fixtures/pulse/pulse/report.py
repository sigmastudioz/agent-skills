from itertools import islice
from .engine import analyze
from .recipe import expand


def build(program):
    return {"metrics": analyze(program), "preview": list(islice(expand(program), 8))}
