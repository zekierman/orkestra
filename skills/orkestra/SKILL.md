---
name: orkestra
description: Coordinate several CLI coding agents (Claude Code, Codex, Antigravity/agy, others) running side by side in herdr panes — discover which agents are available, hand them well-specified tasks, collect results through files, verify claims, and synthesize. Use when the session runs inside herdr (HERDR_ENV=1) with other agent panes and the user asks to involve them ("codex'e sor", "agy'ye baktır", "diğer ajanlara da incelet", "paralel araştır", "ikinci görüş al"), or when a task clearly benefits from independent research, an independent review, or a second opinion. Not for single-agent work.
---

# Orkestra

You are the coordinator. Other agents run in neighbouring herdr panes; you give them bounded
tasks, get their results back through files, check what they claim, and give the user one
synthesized answer. Delegation is only worth it when it buys independence (a second opinion that
didn't see your reasoning), parallel time, or a capability you lack. Otherwise do it yourself.

Commands and per-agent quirks: `references/agents.md`. Known failures and their fixes:
`references/pitfalls.md` — read it before your first dispatch in a session.

## 1. Know the room

Check `HERDR_ENV=1` first; outside herdr, don't touch any session. Then list agents in your own
workspace (`herdr agent list`, filter by `$HERDR_WORKSPACE_ID`, skip `$HERDR_PANE_ID`). A session
start hook may already have given you this roster — trust it only as a starting point, states change.

Default roles (override with whatever the user prefers):

| Agent | Give it | Avoid |
| --- | --- | --- |
| Codex (GPT-6) | deep research, root-cause analysis, code review, reading large codebases | trivial lookups (quota) |
| agy (Gemini Flash) | fast exploration, doc/source discovery, alternative ideas, its own tool docs | final verdicts without checking |
| You (Claude) | decomposition, specs, verification, synthesis, talking to the user | doing everything alone when independence matters |

**Budget:** default one worker. Add a second only for truly independent work or a deliberate second
opinion. Watch quota warnings in pane footers (e.g. Codex "5h limit: 38% left") and say so.

## 2. Write the task spec

Every dispatch is a self-contained spec — the worker has none of your context:

```
TASK <id>  (e.g. T3-review-kavra)
Goal: <one sentence>
Mode: READ-ONLY except the result file. Do not edit, move, or create other files.
Inputs: <absolute paths / URLs — verified to exist right now; include version or commit>
Deliver: write your answer to <result file>, then end it with a final line "DONE <id>".
Format: <e.g. max 10 findings, one line each: file:line — problem — fix; cite URL/file for every claim>
Limits: <time/scope>; if blocked, write "BLOCKED <id>: <why>" to the result file.
```

- **Result files live outside any vault or repo** (a temp/scratch dir), so memory systems and git
  don't pick up worker scratch.
- **Long inputs go in a file; the prompt points to it.** Large pastes stall (`agent_prompt_stalled`).
- **Pin the version** (commit hash, file mtime) so a worker can't review a stale copy.
- Ask for evidence on every claim: file:line or URL. Unsourced "research shows…" gets discarded.
- For a second opinion, don't show your own conclusion first.

## 3. Dispatch and wait

- Send without `--wait` to run workers in parallel, then wait on each:
  `herdr agent wait <target> --until idle --until done --timeout <ms>`.
- **Idle is not done.** Confirm the result file ends with `DONE <id>`; fall back to reading the
  screen (`herdr agent read … --source recent-unwrapped`) only if the file is missing.
- **Don't change inputs while workers read them** (no moves, renames, rewrites mid-task). If you must,
  tell every worker the new path.
- Tell the user in one line which pane got which task.
- If a worker shows a **blocked** dialog (permissions, update prompt, trust review), read it and
  **ask the user** — never pick an option on their behalf.

## 4. Verify, then synthesize

- Spot-check the claims that would change a decision: open the file:line, fetch the URL, run the
  command. A worker saying "tests pass" is a claim, not a result.
- Reject findings about a stale version, findings without evidence, and scope creep.
- Report to the user as: what each agent found → what you accepted, rejected, and why → the decision.
  Surface real disagreements instead of averaging them away.

## 5. Keep the room healthy

- A worker that loaded config at startup (instructions, hooks, memory) won't see changes until its
  **process** restarts; a "new chat" command is not enough.
- Starting / restarting an agent: `herdr agent start <name> --kind <kind> --pane <pane>`; see
  `references/agents.md` for clean exits per agent.
- **Launch flags are a user setting.** If `~/.orkestra/launch.json` exists (e.g.
  `{"agy": ["--dangerously-skip-permissions"]}`), pass that agent's flags after `--` every time you
  start or restart it: `herdr agent start agy --kind agy --pane <pane> -- --dangerously-skip-permissions`.
  Without that file (or an explicit user request), never add permission-bypass flags yourself.
- Don't close or repurpose panes you didn't create unless the user asks.
