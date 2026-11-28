# Follow-Through

**Stop coding agents losing unfinished work.** By [Lex from SigmaStudioz](https://github.com/sigmastudioz). MIT.

Ask an agent for five things, change topic halfway, and the context gets compacted: two of the five quietly
disappear. Plans get replaced on every pivot, summaries drop details, and "sorted into a watch-later bucket"
gets counted as done. Follow-Through moves the record out of the conversation into a small task tree on disk.

- **Every task has a done-when check** and closes only with evidence that it passed.
- **A parent cannot close while a child is open**, so routing work is never mistaken for doing it.
- **Pivots park, never replace:** the current task keeps its exact next step.
- **Only you drop work:** the tree records your words when you do.
- **Optional Claude Code hooks** put the open tree back after a resume or compaction, name open tasks on
  every prompt, and send the agent back once if it tries to stop with a task still in progress.

Standard-library Python 3.8+, local files only, no network. The tree lives in `~/.follow-through/`,
outside your repository.

## Install

```sh
npx skills add sigmastudioz/agent-skills --skill follow-through
```

Or register this repository as a Claude Code plugin marketplace and install `follow-through`.
The hooks are opt-in: see [the skill](skills/follow-through/SKILL.md#hooks-claude-code-optional-installed-by-the-owner)
for the three entries to merge into your settings. Without hooks, the skill and script still work in any
agent that can run a shell command.

## What it guarantees, and what it does not

It guarantees **visibility**: unfinished work keeps coming back into view, after pivots, resumes and
compaction, until it is closed with evidence or you drop it. It does not force the work to happen, and the
evidence is the agent's own statement, so you stay the judge. The tree only knows tasks that were added to
it, and two sessions in one project share one tree. Details are in the skill.
