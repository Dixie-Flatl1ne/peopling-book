# External corroboration — published metrics

Source: Stefan van der Wel, *"OpenClaw: Operating Memory Across Chats, Projects,
and Work"*, LinkedIn (published 2026-05-17).

These are the author's own published figures for the same system. Reproduced here
as external corroboration for the Chapter 7 evidence pack. Numbers differ slightly
from the live 2026-06-04 queries because the corpus is live and growing
(92,366 messages at publication → 98,342 on 2026-06-04).

## Engagement / reliability

- **7,205 direct addresses** to the system (messages explicitly addressing it by
  name, mention, or activation phrase). 4,494 from Stefan, 2,711 from 34
  collaborators (28 human).
- **~87%** of responses needed no rectification; **~5%** drew an explicit
  correction; **~13%** needed correction or follow-up adjustment.
- On memory-dependent asks (prior context mattered), the no-rectification rate
  was still **~83%**.

## Recall performance

- **75 pure chat-history recall asks** from 9 resolved people; 66 answered within
  five minutes; median first response **~29 seconds**; **88%** timely-response
  rate.
- **166 broader recollection requests** (chat, files, email, project facts) from
  12 resolved people; 141 answered within five minutes; median first response
  **~34 seconds**; **~95%** of timely answers needed no correction.

## Corpus / facts (at publication)

- **92,366 messages** — WhatsApp (70,750) + Discord (21,616).
- **2,797 curated work-history records** — actions, events, decisions,
  corrections promoted out of raw chat after validation.
- **26,627 candidate facts** extracted; **8,154 accepted** at publication.
  (Live 2026-06-04: 27,596 candidate / 13,340 accepted.)
- **482 Gmail triage prompts**; **96+ Gmail triage runs created Todoist tasks**;
  **79 live LifeAdmin/WORK admin tasks**.

## Architecture (author's framing)

- Postgres = source of truth (raw messages, candidate + accepted facts,
  validation, provenance, chat scope, access rules, ledgers).
- Obsidian = readable knowledge model (person/chat/project/idea/entity pages).
- QMD = hybrid search layer over the wiki; retrieval, not authority.
- Access control = structural ABAC: who is asking, which channel, which chat the
  fact came from, what scope applies, whether it can cross rooms. "This is what
  makes shared memory useful without making it a leak."
