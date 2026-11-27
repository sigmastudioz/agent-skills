#!/usr/bin/env python3
"""SessionStart hook: if the lean setup's last refresh is older than 7 days, run --refresh
detached in the background (never delays the session; output to refresh.log)."""
import datetime, os, subprocess, sys
LIB = os.path.expanduser("~/.claude/skill-library")
stamp = os.path.join(LIB, "last-refresh")
try:
    last = datetime.datetime.fromisoformat(open(stamp).read().strip())
    if datetime.datetime.now() - last < datetime.timedelta(days=7):
        sys.exit(0)
    open(stamp, "w").write(datetime.datetime.now().isoformat())  # claim before spawning: one refresher
    subprocess.Popen([sys.executable, os.path.join(LIB, "slipstream/scripts/lean_setup.py"), "--refresh"],
                     stdout=open(os.path.join(LIB, "refresh.log"), "a"), stderr=subprocess.STDOUT,
                     stdin=subprocess.DEVNULL, start_new_session=True)
except Exception:
    pass
