#!/usr/bin/env python3
"""Matched, isolated tool-enabled coding trial. Preparation never calls a model."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import random
import shutil
import signal
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("stark_pilot_shared", HERE / "run_pilot.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
digest, write_json, parse_stream = shared.digest, shared.write_json, shared.parse_stream
SKIP = {".git", "__pycache__", ".pytest_cache", ".cursor"}
COMMON = """Work only in this isolated synthetic repository. Read AGENTS.md and README.md, implement
the ticket, and run appropriate local checks. Preserve public interfaces and existing test
expectations. You may inspect/edit package code, add regression tests and an optional short local
note; the README contracts and supplied guidance inputs are read-only. Do not use external files,
global skills/plugins, network research, installs, new dependencies, extra agents, background jobs,
commits, publishing or deployment. Git inspection and standard-library local test commands are
allowed. Other independent workers and the coordinator are active; preserve their work by staying
inside your own checkout. Stop within 1200 seconds. Emit short MILESTONE inspect/repair/verify
updates and a final stdout summary of changed paths, actual commands/results and remaining proof,
ending DONE. Do the coding in the checkout, not as a proposed patch in the final response.
"""
BASELINE = """# Shared engineering defaults

The ticket and contracts are in README.md. Keep the implementation within this repository.
Relevant domain-engineering defaults: keep rules and authoritative writes with their owner;
reuse existing capabilities; preserve public behavior outside scope; trace callers, dependencies,
downstream consumers and relevant failure paths; run checks appropriate to the change. Distinguish
observations, assumptions and actual execution. This instruction does not authorize extra agents,
external actions or unrelated restructuring. These are the supplied relevant baseline contents;
do not read outside this checkout to load a global skill or other instruction file.
"""
TICKETS = {
    "relay": "Fix Local Relay so interrupted delivery and competing workers recover correctly. Preserve the README contracts and CLI. Add appropriate regressions and verify the actual result.",
    "importer": "Finish Restartable CSV Import so interrupted batches resume safely and the CLI reports the durable result accurately. Preserve the README contracts and add appropriate regressions.",
}


def files_in(root):
    files = []
    for path in sorted(root.rglob("*")):
        if SKIP.intersection(path.relative_to(root).parts) or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError("Refusing to follow a supplied or worker-created symlink: " + str(path))
        if path.is_file():
            files.append(path)
    return files


def hashes(root):
    return {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in files_in(root)}


def git(args, cwd):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True, stderr=subprocess.PIPE).strip()


def cursor_command(job):
    return ["agent", "--print", "--model", job["model"], "--auto-review", "--sandbox", "enabled",
            "--trust", "--workspace", job["workspace"], "--output-format", "stream-json"]


def prepare(output, models, profile=None):
    if output.exists():
        raise ValueError("Refusing to overwrite a trial")
    profile = profile or {}
    model_count = profile.get("model_count", 2)
    if len(models) != model_count or len(set(models)) != model_count:
        raise ValueError("Profile requires " + str(model_count) + " distinct explicit model IDs")
    guide_paths = profile.get("guides", [shared.PLUGIN_ROOT / "skills/what-if-tony-stark-built-this/references/coding-loop.md"])
    guide = b"\n\n".join(path.read_bytes() for path in guide_paths)
    tickets = profile.get("tickets", TICKETS)
    fixtures = profile.get("fixtures", HERE / "tool-fixtures")
    checker = profile.get("checker", HERE / "tool_checks.py")
    protocol = profile.get("protocol", HERE / "TOOLS_PROTOCOL.md")
    common = profile.get("common", COMMON)
    guidance_file = profile.get("guidance_file", ".stark-coding-guidance.md")
    assets = profile.get("assets", [])
    asset_hashes = {item["target"]: digest(item["source"].read_bytes()) for item in assets}
    if len(asset_hashes) != len(assets):
        raise ValueError("Duplicate supplied asset target")
    if len(tickets) != 2 or Path(guidance_file).name != guidance_file:
        raise ValueError("Two tasks and a contained guidance filename required")
    output.mkdir(parents=True)
    for name in ("bases", "workspaces", "control", "outputs", "snapshots"):
        (output / name).mkdir()
    owner_root = HERE.parents[2]
    identity = {key: git(["config", key], owner_root) for key in ("user.name", "user.email")}
    bases = {}
    for task in tickets:
        source, base = fixtures / task, output / "bases" / task
        base.mkdir()
        for path in files_in(source):
            dest = base / path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
        (base / "AGENTS.md").write_text(BASELINE)
        (base / ".gitignore").write_text("__pycache__/\n*.pyc\n*.db\n*.sqlite\n")
        git(["init", "-q"], base)
        git(["add", "."], base)
        git(["-c", "core.hooksPath=/dev/null", "-c", "commit.gpgSign=false",
             "-c", "user.name=" + identity["user.name"], "-c", "user.email=" + identity["user.email"],
             "commit", "-qm", "test: seed isolated " + task + " fixture"], base)
        bases[task] = {"path": str(base), "revision": git(["rev-parse", "HEAD"], base), "files": hashes(base)}
    pairs = [(model, task) for model in models for task in tickets]
    random.Random(20261114).shuffle(pairs)
    jobs = []
    for model, task in pairs:
        order = (False, True) if (models.index(model) + list(tickets).index(task)) % 2 == 0 else (True, False)
        for treatment in order:
            identifier = uuid.uuid4().hex[:12]
            workspace = output / "workspaces" / identifier
            subprocess.run(["git", "clone", "--no-local", "-q", bases[task]["path"], str(workspace)], check=True)
            assert git(["rev-parse", "HEAD"], workspace) == bases[task]["revision"]
            assert hashes(workspace) == bases[task]["files"]
            if treatment:
                (workspace / guidance_file).write_bytes(guide)
                (workspace / guidance_file).chmod(0o444)
                for item in assets:
                    target = workspace / item["target"]
                    if (target.is_absolute() and workspace.resolve() not in target.resolve().parents
                            or ".git" in Path(item["target"]).parts or target.exists()):
                        raise ValueError("Supplied asset must be new and contained in the workspace")
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(item["source"].read_bytes())
                    target.chmod(0o444)
            handoff = {
                "goal": tickets[task], "limits": common, "workspace": str(workspace),
                "revision": bases[task]["revision"], "owns": profile.get("owns", "This checkout's package and added regression tests; no other checkout or shared inputs"),
                "interfaces": "Authoritative public APIs, consumers and contracts are in this checkout's README and source",
                "state": profile.get("state", "Committed synthetic base; original public checks pass (relay 3, importer 2); no proposed fix or hidden tests supplied"),
                "evidence": "Only README, source, public tests and local observations; no prior model results supplied",
                "next": "Inspect and implement the ticket within the given bounds",
                "return": {"paths": "Name changed paths", "contracts": "Explain supported public behavior",
                           "checks": "Report commands and actual results", "gaps": "Name remaining defects or uncertainty",
                           "remaining": "Give precise missing proof and stop state"},
                "trace": "Follow the real CLI/service input, state owner, effects and terminal consumer, including relevant failure/recovery",
                "checks": profile.get("checks", "Run python3 -m unittest discover -s tests -v; add relevant regressions without changing existing expectations"),
                "baseline": str(workspace / "AGENTS.md"),
                "isolation": {"confirmed": True, "workspace": str(workspace),
                              "reason": "Independent writable clone of the identified committed synthetic base; no shared source owner"},
            }
            condition = ("Also read and apply " + guidance_file + ". It is the only supplied Stark guidance; do not load any other skill resource."
                         if treatment else "Use your normal engineering reasoning and the shared defaults. No additional skill guidance is supplied.")
            if treatment and profile.get("asset_instruction"):
                condition += " " + profile["asset_instruction"]
            prompt = "HANDOFF_JSON=" + json.dumps(handoff) + "\n\n" + common + "\n" + condition + "\n\nTICKET: " + tickets[task] + "\n"
            (output / "control" / (identifier + ".prompt.txt")).write_text(prompt)
            jobs.append({"id": identifier, "model": model, "task": task, "condition": "relevant" if treatment else "none",
                         "workspace": str(workspace), "base_revision": bases[task]["revision"],
                         "ticket_sha256": digest(tickets[task].encode()), "prompt_sha256": digest(prompt.encode()),
                         "prompt_bytes": len(prompt.encode()), "guidance_bytes": len(guide) if treatment else 0,
                         "guidance_file": guidance_file, "supplied_assets": asset_hashes if treatment else {}})
    manifest = {"protocol": profile.get("name", "tools-enabled-selected-guidance-v1"), "maximum_calls": len(jobs), "maximum_active": profile.get("maximum_active", 3),
                "attempts_per_cell": 1, "timeout_seconds": profile.get("timeout_seconds", 1200), "bases": bases, "jobs": jobs,
                "guide_sha256": digest(guide), "guide_source": [str(path.relative_to(shared.PLUGIN_ROOT)) for path in guide_paths],
                "guidance_sources": {str(path.relative_to(shared.PLUGIN_ROOT)): digest(path.read_bytes()) for path in guide_paths},
                "checker_source": checker.name, "checker_sha256": digest(checker.read_bytes()),
                "asset_sources": {str(item["source"].relative_to(shared.PLUGIN_ROOT)): digest(item["source"].read_bytes()) for item in assets},
                "protocol_sha256": digest(protocol.read_bytes())}
    write_json(output / "control/manifest.json", manifest)
    write_json(output / "control/state.json", {job["id"]: "prepared" for job in jobs})
    print("Prepared " + str(len(jobs)) + " isolated cells; selected guidance/assets, no evaluator files supplied", flush=True)
    return manifest


def execute(output, job, timeout):
    identifier = job["id"]
    target = output / "outputs" / (identifier + ".json")
    if target.exists():
        return json.loads(target.read_text())
    marker = output / "control" / (identifier + ".attempted")
    if marker.exists():
        return {"status": "interrupted-no-rerun"}
    marker.write_text("One model process authorized\n")
    prompt = output / "control" / (identifier + ".prompt.txt")
    assert digest(prompt.read_bytes()) == job["prompt_sha256"]
    workspace = Path(job["workspace"])
    started = time.monotonic()
    print("START " + identifier, flush=True)
    status, code = "completed", None
    with prompt.open() as stdin, (output / "outputs" / (identifier + ".stream.jsonl")).open("w") as stdout, \
            (output / "outputs" / (identifier + ".stderr.txt")).open("w") as stderr:
        process = subprocess.Popen(cursor_command(job), cwd=workspace, stdin=stdin, stdout=stdout, stderr=stderr,
                                   start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            status = "timeout"
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
    parsed = parse_stream((output / "outputs" / (identifier + ".stream.jsonl")).read_text())
    if code not in (0, None):
        status = "process-error"
    snapshot = output / "snapshots" / identifier
    snapshot.mkdir()
    for path in files_in(workspace):
        relative = path.relative_to(workspace)
        if relative.as_posix() == job.get("guidance_file", ".stark-coding-guidance.md"):
            continue
        dest = snapshot / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    diff = subprocess.run(["git", "diff", "--no-ext-diff", "--binary", "HEAD"], cwd=workspace, capture_output=True, text=True)
    (output / "outputs" / (identifier + ".diff")).write_text(diff.stdout)
    final_status = git(["status", "--short"], workspace)
    starts = [e for e in parsed["tool_events"] if e.get("subtype") == "started"]
    result = {"id": identifier, "status": status, "exit_code": code, "elapsed_seconds": round(time.monotonic()-started, 3),
              "response": parsed["response"], "provider_usage": parsed["provider_usage"],
              "recorded_tool_events": len(parsed["tool_events"]), "tool_starts": len(starts),
              "git_status": final_status, "snapshot_files": hashes(snapshot)}
    write_json(target, result)
    print("DONE " + identifier + " " + status + " tool-starts=" + str(len(starts)), flush=True)
    return result


def run(output, workers=3):
    if not 1 <= workers <= 3:
        raise ValueError("At most three concurrent cells")
    manifest = json.loads((output / "control/manifest.json").read_text())
    if workers > manifest.get("maximum_active", 3):
        raise ValueError("Concurrency exceeds this trial's frozen limit")
    checker = HERE / manifest.get("checker_source", "tool_checks.py")
    assert checker.parent.resolve() == HERE.resolve()
    assert digest(checker.read_bytes()) == manifest["checker_sha256"]
    state = json.loads((output / "control/state.json").read_text())
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = {pool.submit(execute, output, job, manifest["timeout_seconds"]): job for job in manifest["jobs"]}
        for future in as_completed(jobs):
            job = jobs[future]
            try:
                state[job["id"]] = future.result()["status"]
            except Exception as error:
                state[job["id"]] = "coordinator-error: " + str(error)
            write_json(output / "control/state.json", state)
    print("All coding cells settled; snapshots await inspection and frozen grading", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models", nargs=2)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if args.action == "prepare":
        if not args.models:
            parser.error("prepare requires --models")
        prepare(args.output.resolve(), args.models)
    else:
        run(args.output.resolve(), args.workers)


if __name__ == "__main__":
    main()
