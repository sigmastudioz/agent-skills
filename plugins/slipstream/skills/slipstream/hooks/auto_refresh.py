#!/usr/bin/env python3
"""SessionStart hook: if the lean setup's last refresh is older than 7 days, run --refresh
detached in the background (never delays the session; output to refresh.log)."""
import datetime, os, subprocess, sys
LIB = os.path.expanduser("~/.claude/skill-library")
stamp = os.path.join(LIB, "last-refresh")
def spawn(*args):
    subprocess.Popen([sys.executable, *args], stdout=open(os.path.join(LIB, "refresh.log"), "a"),
                     stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)


try:
    # New skill or plugin since the catalog was built: rebuild the catalog now (fast), not next week.
    cat = os.path.join(LIB, "catalog.tsv")
    home = os.path.expanduser("~")
    watched = [f"{home}/.claude/skills", f"{home}/.claude/settings.json", f"{home}/.claude/plugins",
               f"{home}/.codex/skills", f"{home}/.agents/skills"]
    if os.path.exists(cat) and any(os.path.exists(w) and os.path.getmtime(w) > os.path.getmtime(cat) for w in watched):
        spawn(os.path.join(LIB, "slipstream/scripts/build_catalog.py"), "--out", cat)
except Exception:
    pass

try:
    last = datetime.datetime.fromisoformat(open(stamp).read().strip())
    if datetime.datetime.now() - last < datetime.timedelta(days=7):
        sys.exit(0)
    open(stamp, "w").write(datetime.datetime.now().isoformat())  # claim before spawning: one refresher
    spawn(os.path.join(LIB, "slipstream/scripts/lean_setup.py"), "--refresh")
except Exception:
    pass
