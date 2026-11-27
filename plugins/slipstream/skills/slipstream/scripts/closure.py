"""Skills a listed skill depends on: any catalog skill named (hyphenated, exact) in its SKILL.md
or in the global instruction files. Process skills are reached by chaining, not by prompt words."""
import os, re
HY = re.compile(r"(?<![a-z0-9-])[a-z0-9]+(?:-[a-z0-9]+)+(?![a-z0-9-])")
_refs = {}


def refs(path, names):
    if path not in _refs:
        try:
            _refs[path] = set(HY.findall(open(path, errors="ignore").read().lower())) & names
        except OSError:
            _refs[path] = set()
    return _refs[path]


def closure(core, paths, extra_text=""):
    names = set(paths)
    out = set(core) | (set(HY.findall(extra_text.lower())) & names)
    todo = list(out)
    while todo:
        s = todo.pop()
        for n in refs(paths[s], names) if s in paths else ():
            if n not in out:
                out.add(n); todo.append(n)
    return out
