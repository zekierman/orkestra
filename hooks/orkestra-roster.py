#!/usr/bin/env python3
"""SessionStart hook: tell the orchestrator which agents share its herdr workspace.

Prints one or two lines of context when running inside herdr with other agent panes;
prints nothing otherwise. Never fails the session: every error path exits 0.
"""
import json
import os
import subprocess
import sys


def roster():
    if os.environ.get("HERDR_ENV") != "1":
        return None
    me = os.environ.get("HERDR_PANE_ID", "")
    ws = os.environ.get("HERDR_WORKSPACE_ID", "")
    out = subprocess.run(["herdr", "agent", "list"], capture_output=True, text=True, timeout=5).stdout
    agents = json.loads(out)["result"]["agents"]
    others = [a for a in agents if a.get("workspace_id") == ws and a.get("pane_id") != me]
    if not others:
        return None
    listed = ", ".join(f"{a['agent']} {a['pane_id']} ({a.get('agent_status', '?')})" for a in others)
    return (f"herdr: you are pane {me}. Other agents in this workspace: {listed}. "
            "For multi-agent work (research, review, second opinions) use the orkestra skill.")


if __name__ == "__main__":
    try:
        sys.stdin.read()
        line = roster()
        if line:
            print(line)
    except Exception:
        pass  # ponytail: a roster is a convenience; never block session start
    sys.exit(0)
