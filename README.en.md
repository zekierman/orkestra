# orkestra

An agent skill for running several coding agents side by side in herdr under one coordinator.
Claude Code conducts; Codex and Antigravity (agy) are the workers. Claude knows who is in the room
on its own, hands out tasks with a precise spec, collects results from files, checks the claims and
gives you one answer.

> Türkçe: [README.md](README.md)

## What it does

- **Knows the room.** A small session-start hook tells Claude which other agents share its herdr
  workspace (pane, status). Outside herdr it prints nothing, and it never breaks a session.
- **Knows who gets what.** Deep research, root-cause analysis and code review go to Codex; fast
  exploration, source discovery and alternative ideas go to agy; decomposition, verification and
  synthesis stay with Claude. One worker by default; a second only for truly independent work or a
  deliberate second opinion.
- **Every task is a self-contained spec.** The worker has none of your context, so each task has an
  id, a one-sentence goal, a read-only rule, verified input paths, a result file and an end marker
  (`DONE <id>`).
- **Results come from files, not the screen.** The worker writes its answer to a file ending in
  `DONE <id>`. An idle pane is not a finished task.
- **Claims get verified.** "Tests pass" is a claim, not a result. Anything that would change a
  decision is checked: file:line, URL, command. Findings without evidence, about a stale version or
  out of scope are dropped.
- **One answer.** What each agent found → what was accepted, rejected and why → the decision. Real
  disagreements are surfaced, not averaged away.
- **Keeps the room healthy.** Permission, update or trust dialogs go to you; it never picks for you.
  Permission-bypass flags only when you asked for them (`~/.orkestra/launch.json`).

## Install

The coordinator is Claude Code. Codex and agy are workers and need nothing installed.

### Claude Code plugin

```
/plugin marketplace add zekierman/orkestra
/plugin install orkestra@orkestra
```

The plugin installs the skill and the room hook together. The hook runs with `python3`, falling
back to `python`.

### Manual

```bash
git clone https://github.com/zekierman/orkestra
cp -r orkestra/skills/orkestra ~/.claude/skills/
cp orkestra/hooks/orkestra-roster.py ~/.claude/hooks/
```

Add to `hooks.SessionStart` in `~/.claude/settings.json`:

```json
{"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/orkestra-roster.py", "timeout": 10}]}
```

On Windows use the full python path. Don't install both: with the plugin, remove the manual hook or
the room is reported twice.

### Launch flags (optional)

To always start an agent with certain flags, write `~/.orkestra/launch.json`:

```json
{"agy": ["--dangerously-skip-permissions"]}
```

orkestra passes them whenever it starts or restarts that agent. Without the file it never adds a
permission-bypass flag on its own.

## Usage

Open a herdr workspace: Claude Code in one pane, Codex and agy beside it. Then just say "ask codex
too", "have agy look at the sources", "get a second opinion", "research this in parallel". Claude
tells you in one line which pane got which task, waits, verifies and reports.

## Limits

- Needs herdr; outside it the skill and hook stay quiet.
- Only Claude Code coordinates. Codex and agy have no hook; they work as workers.
- Workers spend quota. orkestra uses one worker by default and reports quota warnings from pane
  footers.
- Early release. Failures met in real sessions and their fixes are in
  [`references/pitfalls.md`](skills/orkestra/references/pitfalls.md). Open an issue if you hit one.

## License

MIT
