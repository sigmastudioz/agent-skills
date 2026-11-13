#!/usr/bin/env python3
"""Prepare and run the explicit 16-cell Cursor instruction-ablation pilot. Standard library only."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import hashlib
import json
import random
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent
SLUG = "what-if-tony-stark-built-this"
COMMON = """Use only the inline synthetic task and supplied instructions. No tools, file reads,
shell commands, global skill/plugin loading, network research, installs, extra agents or writes.
You are not alone; other isolated runs and the coordinator are active. Own no shared files.
Relevant engineering defaults supplied inline: preserve task scope and public contracts, keep
rules with their owner, trace relevant callers/dependencies/consumers and failure paths, distinguish
facts/assumptions/proposed checks, and do not claim execution. The full engineering baseline is
outside this packet and must not be opened. Return the requested complete artifact to stdout;
the coordinator captures it and executes any authorized local checks separately. Include a brief
MILESTONE inputs-read line, then the requested JSON object, then DONE. No scoring criteria or prior
results are provided. For reasoning tasks, concrete mechanisms and tradeoffs matter, not length.
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def runtime_payload(skill):
    """Supply runtime guidance only; the maintained evaluation pointer is removed exactly once."""
    paths = [skill / "SKILL.md", *sorted((skill / "references").glob("*.md")),
             skill / "assets/experiment-packet.template.md"]
    blocks, hashes = [], {}
    pointer = ("Maintainers only: [evaluation requests and scoring criteria](tests/README.md).\n"
               "Do not load these criteria during ordinary skill use or as an agent under evaluation.\n")
    for path in paths:
        raw = path.read_bytes()
        body = raw.decode()
        relative = path.relative_to(skill).as_posix()
        hashes[relative] = digest(raw)
        if relative == "SKILL.md":
            if body.count(pointer) != 1:
                raise ValueError("Evaluation pointer changed; review the packet transformation")
            body = body.replace(pointer, "")
        blocks.append(f"### Runtime resource: {relative}\n{body}")
    return "\n\n".join(blocks), hashes


def prepare(output, models, seed=20261112):
    if output.exists():
        raise ValueError("Refusing to overwrite an existing pilot; resume with run")
    if len(models) != 2 or len(set(models)) != 2:
        raise ValueError("This bounded pilot requires exactly two distinct model IDs")
    tasks = json.loads((HERE / "tasks.json").read_text())
    if len(tasks) != 4 or len({t["id"] for t in tasks}) != 4:
        raise ValueError("Review protocol before changing the four-task design")
    payload, hashes = runtime_payload(HERE.parent / "skills" / SLUG)
    output.mkdir(parents=True)
    for name in ("control", "packets", "outputs"):
        (output / name).mkdir()
    pairs = [(model, task, index) for model in models for index, task in enumerate(tasks)]
    random.Random(seed).shuffle(pairs)
    jobs = []
    for model, task, index in pairs:
        order = [False, True] if (index + models.index(model)) % 2 == 0 else [True, False]
        for treatment in order:
            identity = uuid.uuid4().hex[:12]
            workspace = output / "packets" / identity
            workspace.mkdir()
            workspace.chmod(0o555)
            handoff = {
                "goal": task["title"], "limits": COMMON, "workspace": str(workspace),
                "revision": digest(task["prompt"].encode()), "owns": "No files; stdout artifact only",
                "interfaces": "The complete synthetic public contract is inline in TASK below",
                "state": "Fresh independent run; no prior output, proposed answer or test rubric supplied",
                "evidence": "Inline source/observations only; proposed checks are not executed evidence",
                "next": "Complete TASK within its scope and output contract",
                "return": {"paths": "Use supplied synthetic symbols", "contracts": "Preserve public task contracts",
                           "checks": "Explain proposed checks without claiming execution",
                           "gaps": "Identify supported uncertainty when relevant", "remaining": "State limits in rationale/analysis"},
                "trace": "Task inputs -> owned behavior -> affected consumers; relevant rejection/recovery",
                "checks": "No tools or execution; coordinator separately checks the returned artifact",
                "baseline": str(Path.home() / ".agents/skills/domain-driven-design/SKILL.md"),
                "isolation": {"confirmed": True, "workspace": str(workspace),
                              "reason": "Fresh empty read-only packet; all authorized synthetic input is inline"},
            }
            instructions = ("Apply the following supplied skill runtime instructions within TASK scope:\n" + payload
                            if treatment else "Complete TASK using your normal engineering reasoning and the shared defaults above.")
            prompt = ("HANDOFF_JSON=" + json.dumps(handoff) + "\n\n" + COMMON + "\n\n" + instructions
                      + "\n\n## TASK\n" + task["prompt"] + "\n")
            (output / "control" / f"{identity}.prompt.txt").write_text(prompt)
            jobs.append({"id": identity, "model": model, "task": task["id"], "kind": task["kind"],
                         "condition": "with" if treatment else "without", "workspace": str(workspace),
                         "task_sha256": digest(task["prompt"].encode()), "prompt_sha256": digest(prompt.encode()),
                         "prompt_bytes": len(prompt.encode())})
    manifest = {"protocol": "matched-instruction-ablation-v1", "seed": seed, "maximum_calls": 16,
                "maximum_active": 3, "attempts_per_cell": 1, "common_sha256": digest(COMMON.encode()),
                "tasks_sha256": digest((HERE / "tasks.json").read_bytes()),
                "rubric_sha256": digest((HERE / "rubric.json").read_bytes()), "skill_files": hashes,
                "transformation": "Remove only the two-line maintainer evaluation pointer; exclude tests/evaluation files",
                "jobs": jobs}
    write_json(output / "control/manifest.json", manifest)
    write_json(output / "control/state.json", {job["id"]: "prepared" for job in jobs})
    print(f"Prepared {len(jobs)} frozen cells; mapping remains in coordinator control", flush=True)
    return manifest


def parse_stream(raw):
    final, assistant, tools, usage = "", [], [], None
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") == "tool_call":
            tools.append(event)
        if event.get("type") == "assistant":
            message = event.get("message", {})
            content = message.get("content", []) if isinstance(message, dict) else []
            if isinstance(content, str):
                assistant.append(content)
            elif isinstance(content, list):
                assistant.extend(item.get("text", "") for item in content if isinstance(item, dict))
                tools.extend(item for item in content if isinstance(item, dict) and item.get("type") == "tool_use")
        if event.get("type") == "result":
            value = event.get("result")
            if isinstance(value, str):
                final = value
            usage = event.get("usage", usage)
    return {"response": final or "\n".join(assistant), "tool_events": tools, "provider_usage": usage}


def response_object(text):
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text[index:])
        except ValueError:
            continue
        if isinstance(obj, dict) and any(isinstance(obj.get(k), str) for k in ("code", "analysis")):
            return obj
    return None


def execute_cell(output, job, timeout):
    identity = job["id"]
    result_path = output / "outputs" / f"{identity}.json"
    if result_path.exists():
        return json.loads(result_path.read_text())
    attempt = output / "control" / f"{identity}.attempted"
    if attempt.exists():
        return {"id": identity, "status": "interrupted-no-rerun", "elapsed_seconds": None}
    attempt.write_text("One call authorized for this cell\n")
    prompt = output / "control" / f"{identity}.prompt.txt"
    if digest(prompt.read_bytes()) != job["prompt_sha256"]:
        raise ValueError("Prompt changed after freeze: " + identity)
    command = ["agent", "--print", "--model", job["model"], "--mode", "ask", "--sandbox", "enabled",
               "--trust", "--workspace", job["workspace"], "--output-format", "stream-json"]
    started = time.monotonic()
    print("START " + identity, flush=True)
    code, status = None, "completed"
    with prompt.open() as stdin, (output / "outputs" / f"{identity}.stream.jsonl").open("w") as stdout, \
            (output / "outputs" / f"{identity}.stderr.txt").open("w") as stderr:
        process = subprocess.Popen(command, cwd=job["workspace"], stdin=stdin, stdout=stdout, stderr=stderr)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            status = "timeout"
    elapsed = time.monotonic() - started
    parsed = parse_stream((output / "outputs" / f"{identity}.stream.jsonl").read_text())
    artifact = response_object(parsed["response"])
    if status == "completed" and code != 0:
        status = "process-error"
    if parsed["tool_events"]:
        status = "invalid-tool-use"
    elif status == "completed" and artifact is None:
        status = "unparseable-output"
    result = {"id": identity, "status": status, "exit_code": code, "elapsed_seconds": round(elapsed, 3),
              "response": parsed["response"], "artifact": artifact,
              "response_characters": len(parsed["response"]),
              "tool_event_count": len(parsed["tool_events"]), "provider_usage": parsed["provider_usage"]}
    write_json(result_path, result)
    print("DONE " + identity + " " + status, flush=True)
    return result


def run(output, timeout=600, workers=3):
    manifest = json.loads((output / "control/manifest.json").read_text())
    if not 1 <= workers <= 3 or not 1 <= timeout <= 900:
        raise ValueError("Pilot bounds: at most 3 active calls and 900 seconds per call")
    state = json.loads((output / "control/state.json").read_text())
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(execute_cell, output, job, timeout): job for job in manifest["jobs"]}
        for future in as_completed(futures):
            job = futures[future]
            try:
                state[job["id"]] = future.result()["status"]
            except Exception as error:
                state[job["id"]] = "coordinator-error: " + str(error)
            write_json(output / "control/state.json", state)
    blind = []
    for job in manifest["jobs"]:
        path = output / "outputs" / f"{job['id']}.json"
        if path.exists():
            result = json.loads(path.read_text())
            blind.append({"id": job["id"], "task": job["task"], "status": result["status"],
                          "artifact": result.get("artifact"), "response": result.get("response", "")})
    random.Random(manifest["seed"] + 1).shuffle(blind)
    write_json(output / "blind.json", blind)
    print("All cells settled; condition-masked artifacts ready in blind.json", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--models", nargs=2)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.action == "prepare":
        if not args.models:
            parser.error("prepare requires --models")
        prepare(output, args.models)
    else:
        run(output, args.timeout, args.workers)


if __name__ == "__main__":
    main()
