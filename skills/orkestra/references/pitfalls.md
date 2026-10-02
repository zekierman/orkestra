# Pitfalls (each one happened in a real session)

| What happened | Why | Do instead |
| --- | --- | --- |
| Two workers were reviewing a folder when it got renamed; their paths broke | Inputs changed mid-task | Freeze inputs until every worker reports `DONE`; if you must move, re-send the new path |
| A ~22 KB pasted prompt never started (`agent_prompt_stalled`) | Large bracketed paste | Write long input to a file, prompt with the path |
| `wait` returned while the worker was still thinking | Idle/done state ≠ task complete | Result file + final `DONE <id>` line |
| A reviewer critiqued an older draft | It read a cached/stale copy | Put commit hash or mtime in the spec; reject stale findings |
| A worker cited "OpenAI/Anthropic research shows…" with no source | Plausible filler | Require URL or file:line for every claim; drop unsourced ones |
| Codex couldn't run any shell command | Sandbox failed to start on Windows | Ask the user to change its permission mode |
| Codex still showed old memory after `/new` | Config loads at process start | Restart the process (`ctrl+c` ×2, start again) |
| Sending `2` then Enter to an update dialog chose "Update now" | The key wasn't taken as a selection; Enter hit the default | Never answer dialogs for the user; ask them |
| `codex exec` didn't get memory context | Hooks don't run in exec mode | Use an interactive pane when hooks matter |
| Two workers wrote to one file literally named `dir$2`; the second overwrote the first | A spec built in a bash function escaped `\$2` (Windows path backslash before a variable) | Put each worker's full result path in a plain variable first, check the sent text, and never give two workers the same output name |

## Windows: console windows flashing while Codex works

Codex (0.157 on Windows) runs hook commands through the session shell from a background process that
has no console, without `CREATE_NO_WINDOW` — so every hook run can pop a console window
(`codex-rs/hooks/src/engine/command_runner.rs`). Tool calls may do the same. Nothing in a hook's own
command can hide the outer shell window.

Mitigations: keep Codex hooks to rare events (SessionStart / PreCompact / SessionEnd) instead of
per-prompt/per-tool ones; report it upstream (Codex accepts issues, not external PRs).
