# Chapter 7: November 2026 snapshot

Stefan van der Wel's system, checked 21 November 2026 in Australia/Sydney. This note records what changed after the [September snapshot](september-2026-published-snapshot.md) and supports the revised section "Carry the work between agents". These are observations of the author's system, not an independent evaluation.

## What changed since September

The September snapshot described an engineering sharing service. It delivered selected, checked records into each agent's own memory bank and tracked every delivery. That service no longer runs.

- The system's own documentation records that the engineering sync stopped on 10 October 2026.
- On the server that ran it, both of its timers were found disabled on 21 November 2026.

## Shared engineering memory

Codex, Claude and omp now use one shared engineering memory bank.

- On the Mac where this was checked, the memory configuration used by Codex and Claude and the separate configuration used by omp both name the same single bank.
- Session retention is switched on for Codex and Claude. omp retains after every turn.
- Commit messages from each repository are also ingested.
- Records are tagged with the project they belong to. Records written by Codex and Claude also carry a tag for the agent. omp's own writes carry the project tag only.
- omp's retention instruction says that an assistant's statements about fixes, tests and deployments remain attributed claims unless supported by evidence, and that personal facts are excluded. The system documentation describes equivalent instructions for the other writers.

Hermes reads the shared engineering memory and does not write to it. This is taken from the system documentation, dated 24 October 2026. It is a rule Hermes is instructed to follow. The check did not establish that the server enforces it.

The other machines that run these agents were not inspected on 21 November. The documentation says they receive the identical configuration.

## Corrections

The documentation records two findings from the October clean-up of the shared memory:

- Prefixing a stale fact with "Superseded" did not work, because consolidation rebuilt a present-tense observation from it. Stale facts are invalidated instead.
- A review classified 2,063 older imported notes and retired 645 of them. Of those, 253 were sync bookkeeping (record ids, hashes and revisions), 370 were transient status or one-off test results and 22 had no content.

## Workspace register

A shared workspace policy was approved on 15 October 2026. Agents work in one registered checkout of each project and claim the files they intend to change before editing them.

On 21 November 2026, an agent revising this book began editing an older clone of the repository. It found the registered checkout through the workspace register and moved the change across. The older clone has since been deleted.

## What this does not show

- No measurement was made of how often an agent recalls the right record or uses it correctly.
- Automatic retention means records enter the shared memory without the owner review that the September service required.
- The chapter does not state why the sharing service was replaced, because the documentation consulted does not record a reason.
