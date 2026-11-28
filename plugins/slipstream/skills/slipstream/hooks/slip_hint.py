#!/usr/bin/env python3
"""UserPromptSubmit hook: lazy skill discovery without relying on the model to search.

Matches the user's prompt against the skill catalog. When an archived/unlisted skill's NAME is
mostly covered by the prompt, inject one line pointing at its SKILL.md (~60-100 tokens). Silent
otherwise. Skills already listed (in ~/.claude/skills or the project's .claude/skills) are skipped.
Env: SKILL_CATALOG (default ~/.claude/skill-library/catalog.tsv)."""
import json, os, re, sys

STOP = set("a an the and or for to of in on with my me i we use using how do can this that it is be from into by our "
           "skill skills load loaded would normally reply sentence naming first step not carry out task run help make please".split())


def stems(text):
    ws = [w for w in re.findall(r"[a-z0-9+#]+", text.lower()) if w not in STOP and len(w) > 1]
    return {w[: max(5, len(w) - 3)] if len(w) > 6 else w for w in ws}


def load_index(catalog):
    import math
    rows = [l.rstrip("\n").split("\t") for l in open(catalog, encoding="utf-8", errors="ignore")]
    rows = [r for r in rows if len(r) >= 4 and "/fixtures/" not in r[3] and "/tests/" not in r[3]]
    tok = {r[0]: [t for t in re.split(r"[-_:\s]+", r[0].lower()) if len(t) >= 3] for r in rows}
    df = {}
    for ts in tok.values():
        for t in set(ts):
            df[t] = df.get(t, 0) + 1
    ap = os.environ.get("SKILL_ALIASES", os.path.join(os.path.dirname(catalog), "aliases.json"))
    learned = json.load(open(ap)) if os.path.exists(ap) else {}
    return {"rows": rows, "tok": tok, "idf": {t: math.log(len(rows) / n) for t, n in df.items()},
            "aliases": learned.get("aliases", {}), "unique": set(learned.get("unique", [])),
            "by_name": {r[0]: r for r in rows}, "alias_score": 50.0,
            # rarity floor scales with catalog size (0.9 * ln N == 7.0 at ~2,400 skills)
            "rare_min": 0.9 * math.log(max(len(rows), 2))}



PASTE = re.compile(r"```.*?```|<pasted_content.*?</pasted_content>", re.S)
CARRIED = ("This session is being continued", "Background (from the session", "None of the sessions you started",
           "Another Claude session sent a message")


def own_words(prompt):
    """The user's own request: no code blocks, pasted content or carried-over summaries."""
    if prompt.lstrip().startswith(CARRIED) or "toolu_" in prompt or "<task-notification" in prompt:
        return ""  # carried-over summaries and machine notifications are not the user's request
    return PASTE.sub(" ", prompt)[:400]


def exact_mentions(full, idx, listed):
    """Exact skill names (or joined name parts, e.g. 'shotcraft' for shot-craft) anywhere, summaries included."""
    low = full.lower()
    words = set(re.findall(r"[a-z0-9]+", low))
    out = []
    for p in idx["rows"]:
        n = p[0]
        if n in listed or len(n) < 6:
            continue
        parts = [t for t in re.split(r"[-_:\s]+", n.lower()) if t]
        joined = {"".join(parts[i:j]) for i in range(len(parts)) for j in range(i + 2, len(parts) + 1)}
        if ("-" in n and re.search(rf"(?<![a-z0-9-]){re.escape(n.lower())}(?![a-z0-9-])", low)) or \
                any(len(j) >= 8 and j in words for j in joined):
            out.append((100.0, n, p[2], p[3]))
    return out


NAMED = re.compile(r"((?:[a-z0-9]+[ -]){1,3})skills?\b")


def named_skill(text, idx, listed):
    """'the social media skill', 'our new editor skills': the user is naming a skill."""
    out = []
    for m in NAMED.finditer(text.lower()):
        ws = [w for w in re.split(r"[ -]+", m.group(1)) if w and w not in STOP and len(w) >= 3]
        if not ws:
            continue
        for p in idx["rows"]:
            if p[0] in listed:
                continue
            toks = set(idx["tok"][p[0]])
            desc = set(re.findall(r"[a-z0-9]+", p[2].lower()))
            in_name = sum(any(t.startswith(w[:5]) for t in toks) for w in ws)
            if in_name == len(ws):
                out.append((80.0 + 5 * in_name - len(toks), p[0], p[2], p[3]))
            elif in_name and all(w in desc or any(t.startswith(w[:5]) for t in toks) for w in ws):
                out.append((55.0, p[0], p[2], p[3]))
    return out


APP_BLOCKS = re.compile(r"<(system-reminder|side-sessions-event|task-notification|ci-monitor-event|agent-message)\b.*?</\1>"
                        r"|^\[SYSTEM NOTIFICATION[^\n]*$", re.S | re.M)


def typed_only(prompt):
    """What the user typed: app-generated notices (session events, reminders, task and CI
    notifications, other sessions' hand-backs, carried-over summaries) ride along in the
    prompt but are never the request."""
    if prompt.lstrip().startswith(CARRIED):
        return ""  # a carried-over summary or another session's hand-back, not a typed request
    return APP_BLOCKS.sub(" ", prompt).strip()


def match(prompt, idx, listed):
    prompt = typed_only(prompt)
    if not prompt:
        return []
    exact = exact_mentions(prompt, idx, listed) + named_skill(own_words(prompt), idx, listed)
    prompt = own_words(prompt)
    q = stems(prompt)
    best = []
    words = set(re.findall(r"[a-z0-9+#]+", prompt.lower()))
    for alias, skill in idx.get("aliases", {}).items():  # learned from the local user's history
        if alias in words and skill not in listed and skill in idx["by_name"]:
            r = idx["by_name"][skill]
            best.append((idx["alias_score"], r[0], r[2], r[3]))
    for p in idx["rows"]:
        toks = idx["tok"][p[0]]
        if p[0] in listed or not toks:
            continue
        m = [t for t in toks if any(s == t or (len(s) >= 4 and t.startswith(s)) or (len(t) >= 5 and s.startswith(t[:5]) and len(s) >= 5)
                                    for s in q)]
        cov = len(m) / len(toks)
        rare = sum(idx["idf"][t] for t in m)
        distinct = any(t in idx["unique"] and t in words for t in m)  # exact word, unique to this skill
        # most of the name must match: 2 of 3 words is deliberately not enough (noise, no recall gain)
        if (len(m) >= 2 and cov >= 0.67 and rare >= idx["rare_min"]) or (len(m) == 1 and len(toks) == 1 and len(toks[0]) >= 8 and toks[0] in words) or distinct:
            best.append((max(sum(idx["idf"][t] for t in m) * cov, 60.0 if distinct else 0), p[0], p[2], p[3]))
    best += exact
    best.sort(key=lambda r: -r[0])
    seen, uniq = set(), []
    for b in best:
        if b[1] not in seen:
            seen.add(b[1]); uniq.append(b)
    best = [b for b in uniq[:2] if b[0] >= 0.6 * uniq[0][0]] if uniq else []
    return [(s, 0, n, d, path) for s, n, d, path in best]


def matches(prompt, catalog, listed):
    return match(prompt, load_index(catalog), listed)


def listed_names(cwd):
    names = set()
    roots = os.environ.get("SKILL_LISTED_DIRS")
    roots = roots.split(":") if roots else [os.path.expanduser("~/.claude/skills"), os.path.join(cwd or ".", ".claude/skills")]
    for root in roots:
        if os.path.isdir(root):
            names |= set(os.listdir(root))
    return names


def main():
    try:
        ev = json.load(sys.stdin)
        cat = os.environ.get("SKILL_CATALOG", os.path.expanduser("~/.claude/skill-library/catalog.tsv"))
        hits = matches(ev.get("prompt", ""), cat, listed_names(ev.get("cwd")))
    except Exception:
        return
    if not hits:
        return
    clean = lambda t: re.sub(r"[^\w .,:;()/'+&-]", " ", t)[:110].strip()  # description is data, not markup
    lines = [f"- {clean(n)}: {clean(d)} -> Read {p}" for _, _, n, d, p in hits]
    note = ("slipstream skill-library: installed skill(s) that match this request but are not in the listing. "
            "If one fits the task, Read its SKILL.md and use it as you would a listed skill:\n" + "\n".join(lines))
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": note}}))


if __name__ == "__main__":
    main()
