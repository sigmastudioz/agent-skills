# Engineering invention: change the mechanism, earn the result

Use when the requested outcome is blocked by the present approach. Preserve the outcome and hard
constraints while challenging the means. Start with a compact constraint statement: what must become
possible, what cannot change, and which operation currently grows or fails beyond the available budget.
Ground this in enough source or evidence to choose a mechanism; exhaustive auditing is not a prerequisite.

## Search for a structural escape

A local optimization preserves the expensive work and makes each instance cheaper. Ask whether the
work itself can disappear. Look at the information entering the system, the answer the consumer needs,
and the gap between them. Which details must survive, and which are being generated only to throw away?

| Move | Question to try |
| --- | --- |
| Remove work | Can a maintained invariant or an existing fact make this operation unnecessary? |
| Change representation | Can the required answer be obtained without constructing the current intermediate form? |
| Change granularity | Can a whole region or family be handled together with a correctness argument? |
| Move the decision | Where do sufficient information and legitimate authority already meet? |
| Reverse the direction | Can the desired result constrain the search instead of generating every possibility? |
| Combine capabilities | Do existing partial answers compose into the exact answer the consumer needs? |

These are search prompts, not required architectures. Borrow a mechanism only after checking why its
assumptions hold here. A cache needs a freshness story; deferred work still costs something; moving a
boundary must preserve authority. Include preprocessing, invalidation, storage and recovery costs when
claiming improvement. Adding workers does not remove total work by itself.

## Make the leap executable early

State the proposed mechanism and why it changes the limiting relationship. When a plausible approach
meets the hard constraints, test its decisive part through a small implementation before writing a long
comparison. Explore another candidate when the current one fails a constraint or a real tradeoff remains;
do not delay a viable build to fill an alternatives quota.

Choose a discriminating check: ordinary happy-path success rarely distinguishes the old mechanism from
the new one. Use the workload shape, boundary or failure that makes the old approach untenable, paired
with a correctness oracle or invariant. Check small diverse inputs against a trustworthy simple method
when available, then exercise the scale or boundary the new mechanism is meant to unlock. Do not infer
exactness from speed, or resource behavior from a small correctness example.

Keep a viable slice running while expanding coverage. After the mechanism works, integrate it through
the supported entry and terminal consumer. Remove obsolete work on that path; an optimized core that
feeds an unchanged expensive presenter still fails the user's goal. Stop analysis that cannot change
implementation, acceptance or the choice of mechanism. Honor the task's resource bound.

## Decide from evidence

Compare the outcome with the baseline under matching inputs and semantics. Report what work was
eliminated and what obligations replaced it. Prefer deterministic work/resource evidence where possible;
report wall-time measurements with their environment and limits. Separate a design argument, a checked
prototype and a measured deployment. If the clever idea loses on correctness, complexity or actual
constraints, reject it and retain the simpler supported result. No novelty bonus compensates for a
broken contract. Store the rejected assumption and useful proof with the owning project, not as a new
universal instruction for unrelated tasks.
