# Chapter 7: September 2026 snapshot

Stefan van der Wel's system, checked 14 September 2026 in Australia/Sydney. The UTC collection times fall on 13 September because the checks occurred shortly after midnight AEST. These are observations of the author's system, not an independent evaluation.

## Source communications

A read-only, repeatable-read query of Correspondence's filtered reader view returned the following at 14:19:37 UTC. It counts distinct source-message IDs, excluding material the view does not expose.

| Channel | Visible source messages | Distinct chats or threads |
|---|---:|---:|
| WhatsApp | 93,891 | 158 |
| Gmail | 53,357 | 37,401 |
| Discord | 56,671 | 398 |
| SMS | 30,874 | 1,522 |
| **Total messages** | **234,793** | |

The latest WhatsApp message was timestamped 14:19:32 UTC, about five seconds before collection began. The WhatsApp total included 1,285 messages timestamped on or after 1 September UTC.

These are messages visible through the reader view, not the complete raw database. June's 98,343-message snapshot covered a different channel mix and raw-row scope, so the difference is not a like-for-like growth measure. Chat and thread totals are not counts of people.

## Interpreted memory

The active Hermes memory bank's inventory reported **154,435 valid derived memory records** at 14:17:26 UTC and **7,798 retained source documents** at 14:19:43 UTC.

Derived memory records are interpretations, not independently verified truths or counts of original messages. Retained documents can include historical material and need not correspond one-to-one with communications. These are live endpoint totals from separate reads, not a complete enumeration or a simultaneous snapshot.

## Engineering sharing

The sharing service reported **22 distinct engineering record IDs with completed deliveries** and **49 completed recipient copies**: 22 in Claude's memory, 21 in Codex's and 6 in Hermes's. A further 27 revisions remained held. A completed delivery means the service confirmed the destination copy and its extraction; it does not prove that the receiving agent later recalled it or used it correctly.

## What the architecture now separates

- **Correspondence:** source communications, identity, dates, conversation scope and provenance.
- **Hindsight:** interpreted memory derived from selected material, separate from the older curated-facts audit layer.
- **Agent access:** native memory recall in Hermes, and dedicated memory/source tools in Codex. Agents can have different context and permissions.
- **Engineering distribution:** selected, attributed records delivered to named agent memory banks, with revisions and per-destination delivery tracking. The service does not synchronise every personal memory wholesale.

The configuration, deployed source hashes, active gateway/timers and distributor status were inspected. Those checks establish the observed setup, not an end-to-end security audit or a benchmark of understanding. No new response-accuracy percentage was measured. The May response figures remain historical observations with incomplete evaluation methodology.

The chapter deliberately uses only two rounded quantities in the narration and explains the components through their consequences for the work.
