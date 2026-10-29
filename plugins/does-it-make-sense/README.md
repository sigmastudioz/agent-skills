# Does It Make Sense?

By **[Lex from SigmaStudioz](https://github.com/sigmastudioz)** · MIT · version 1.0.0.

Understand what was actually built and whether the intended user can achieve the original
end goal. Trace from the problem through real entry points, implementation, state changes
and downstream effects to the terminal result. Trace significant components backward to
the outcome or constraint they serve.

## Install

```sh
npx skills add sigmastudioz/agent-skills --skill does-it-make-sense
```

For Claude Code, register this repository and select `does-it-make-sense@sigmastudioz`.
Claude, Cursor and Codex manifests are included. Native marketplace review and activation
are separate; this package has no directory submission or approval implied by its creation.
Normal skill discovery remains enabled, with no global instruction or hook installation.

## Assessment and refinements

The skill explains actual capability, gives a per-goal verdict, and links findings to
specific paths and evidence. It challenges acceptance criteria that can pass while leaving
the user's job unfinished. It separates defects, missing integration, required capability,
goal/criteria mismatch, refinement opportunities and unverified paths.

Each refinement names the goal impact, evidence, smallest sufficient change, responsible
layer or owner, expected behavior and observable closure check. Required corrections,
optional improvements and new product decisions remain separate. No change is a valid
recommendation. A review is read-only; product fixes require authorization within scope.

## Examples and limits

- Review an existing recovery flow: follow retry through to authoritative final state and
  whether the operator can confirm success, then recommend only the missing step.
- Review a completed feature whose tests pass: check whether its criteria establish the
  agreed user outcome without inventing additional features.
- Assess a source-only build: distinguish static conclusions from runtime evidence still
  needed; missing access alone is not a demonstrated product defect.

This package contains instructions and UI metadata, with no executable helper or required
service. It reuses existing project tools and task/gap records rather than creating a new
tracking system. No private evidence is sent to the publisher. See [Privacy](../../PRIVACY.md).

[Skill instructions](skills/does-it-make-sense/SKILL.md) are the operative contract. Structure,
metadata, distribution and authored scenario review can be checked locally; these do not
establish fresh native-agent adherence, complete product verification or directory approval.
