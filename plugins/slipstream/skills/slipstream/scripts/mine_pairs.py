#!/usr/bin/env python3
"""Mine ground truth from history: (user prompt -> skill the agent then loaded), plus
negatives (prompts after which no skill was loaded). Output stays local (default under
~/.claude/skill-library/). Explicit slash commands are excluded: they need no discovery.
Usage: python3 mine_pairs.py [--days 60] [--out pairs.jsonl]"""
import argparse, glob, json, os, re, time
from concurrent.futures import ProcessPoolExecutor

HOME = os.path.expanduser("~")
SKP = re.compile(r"/([^/]+)/SKILL\.md")


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def clean(t):
    t = re.sub(r"<system-reminder>.*?</system-reminder>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def claude(path):
    out, prompt, loaded, ts = [], None, [], ""

    def flush():
        if prompt:
            out.append({"src": "claude", "session": os.path.basename(path), "ts": ts, "prompt": prompt[:1500], "skills": loaded[:3]})

    for raw in open(path, "rb"):
        if b'"type":"user"' not in raw and b'"type":"assistant"' not in raw:
            continue
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if d.get("isSidechain"):
            continue
        m = d.get("message") or {}
        if d.get("type") == "user":
            c = m.get("content")
            if isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                continue
            t = text_of(c)
            if "<command-name>" in t or t.lstrip().startswith("/") or d.get("isMeta") or "<task-notification" in t or "toolu_" in t:
                flush(); prompt, loaded = None, []
                continue
            t = clean(t)
            if len(t) < 12:
                continue
            flush(); prompt, loaded, ts = t, [], d.get("timestamp", "")
        elif d.get("type") == "assistant" and prompt:
            for b in m.get("content") or []:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                if b.get("name") == "Skill":
                    loaded.append(b["input"].get("skill", "").split(":")[-1])
                elif b.get("name") == "Read":
                    mm = SKP.search(b.get("input", {}).get("file_path", ""))
                    if mm:
                        loaded.append(mm.group(1))
    flush()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=60)
    ap.add_argument("--out", default=f"{HOME}/.claude/skill-library/pairs.jsonl")
    a = ap.parse_args()
    cut = time.time() - a.days * 86400
    files = [p for p in glob.glob(f"{HOME}/.claude/projects/*/*.jsonl") if os.path.getmtime(p) >= cut]
    with ProcessPoolExecutor() as ex:
        rows = [r for rs in ex.map(claude, files, chunksize=8) for r in rs]
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    pos = sum(1 for r in rows if r["skills"])
    print(f"{len(rows)} prompts ({pos} followed by a skill load, {len(rows) - pos} without) -> {a.out}")


if __name__ == "__main__":
    main()
