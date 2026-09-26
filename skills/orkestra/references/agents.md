# Agents: commands and quirks

Verify syntax against the installed binaries (`herdr agent`, `codex --help`, `agy --help`) — these
move fast.

## herdr (the room)

| Need | Command |
| --- | --- |
| Am I inside herdr? | `test "$HERDR_ENV" = 1` |
| Who's here | `herdr agent list` (JSON; filter `workspace_id`) |
| Send a task | `herdr agent prompt <name-or-pane> "<spec>"` (add `--wait --timeout <ms>` for a single worker) |
| Wait | `herdr agent wait <target> --until idle --until done --timeout <ms>` |
| Read screen | `herdr agent read <target> --source recent-unwrapped --lines 150` |
| Keys | `herdr agent send-keys <target> esc` / `ctrl+c` / `enter` |
| Start an agent in a shell pane | `herdr agent start <name> --kind codex|agy|claude --pane <pane>` |
| New pane beside you | `herdr pane split --current --direction right --cwd "$PWD" --no-focus` |
| Notify the user | `herdr notification show "<title>" --body "<text>"` |

Screen reads can miss output from agents that use the terminal's alternate screen — another reason
to deliver results through files.

## Codex CLI

- Research/review in a pane works well; give precise completion criteria (it can stop early under
  vague ones).
- **Sandbox:** in some Windows setups its shell fails to start under the default sandbox and it
  can't read files. If a worker reports it can't run commands, ask the user to switch it to a
  permission mode that allows reads (e.g. Full Access) — don't do it for them.
- **Config reload:** global instructions (`AGENTS.md`) and hooks load at process start. `/new`
  doesn't reload them. Exit with `ctrl+c` twice (slash-quit may not exit), then start again.
- **Hooks** need a one-time trust review in the TUI (`/hooks`); any change to a hook command changes
  its hash and needs re-approval.
- **Headless:** `codex exec "<prompt>"` runs one task non-interactively (hooks don't run there).
- Quota shows in the footer ("5h limit: N% left").

## Antigravity CLI (agy)

- Headless, read-only, machine-readable:
  `agy -p "<prompt>" --mode plan --output-format json > result.json`
  (`--print-timeout 0` waits for the full turn; `--json-schema` enforces structure.)
- Continue a thread: `-c` (latest) or `--conversation <id>`.
- `--dangerously-skip-permissions` auto-approves tools — only with the user's consent.
- Strong at quickly reading local docs and scanning sources; check its citations — it can present
  unsourced generalizations as research.
- Quota: shared across Antigravity apps on the same Google account.

## Claude Code (as a worker)

- Headless: `claude -p "<prompt>"` (hooks do run). Useful for quick verification runs.
