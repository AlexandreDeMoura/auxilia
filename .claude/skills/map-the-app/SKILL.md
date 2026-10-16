---
name: map-the-app
description: Fill the knowledge base in `knowledge-base/` from zero, one Area at a time, over several sessions. Use when the Builder asks to map the app, or to carry on a mapping that `knowledge-base/mapping-record.md` records.
---

# Map the app

Mapping fills the knowledge base of an app nobody has described yet. You make an inventory of the app's Entry points and come back with Areas; the Builder picks an Area; you list its Flows, the Builder corrects the list, and you write them one at a time with the `write-a-flow` skill. It takes many sessions, each started by the Builder. What carries the mapping from one session to the next is the Mapping record.

An **Entry point** is a place where something outside the system starts something inside it: a page, an endpoint, a scheduled job, an incoming event. Every Flow starts at one; one Entry point may serve several Flows, and some serve none.

## Say it short

Everything you say to the Builder is short, recommendations above all.

- A message holds what the Builder has to decide now, and what was done. A doubt of yours that changes nothing they decide now goes in the Mapping record.
- A recommendation is one or two lines: the choice, then the reason.
- An Area, a Flow, a Flow to write or a possible bug is one line.
- Whatever is longer lives in the Mapping record or the knowledge base, and your message says where.

The Builder decides on what they read in full. A recommendation too long to read gets skimmed and accepted, and then nobody has decided anything.

## Steps

1. **Look whether `knowledge-base/mapping-record.md` exists**, and read it when it does. Nothing else is read yet.
2. **Give the Builder your opening message**, as text in your reply, before any further tool call. The Builder never sees what you think, so an opening you only thought was not given. Which message it is depends on the record:

   | The Mapping record | Opening message | The session |
   |---|---|---|
   | does not exist | The explanation below. | `inventory.md` |
   | has a row "not looked at yet", a row naming a Flow to write, or `areas.yaml` lists a Flow to write | One line on where the mapping stands ("3 of 9 Areas done, Agents in progress with 4 Flows to write left"). | `area.md` |
   | has neither, and `areas.yaml` lists no Flow to write | One line: every Entry point is accounted for. | `end.md` |

   Done when the message is written out in your reply.
3. **Read the session's file and follow it.**

**The explanation** opens a mapping. The Builder is about to wait while you read their whole app, so they are told what is coming. Say this, in your own words where the app calls for it:

> Mapping the app. I will read the code for every page, endpoint, scheduled job and incoming event, with the docs and tests as a hint for names.
> I will come back with a Mapping record at `knowledge-base/mapping-record.md` and a proposal of Areas for you to correct.
> No Flow is written until you have picked an Area and corrected its list of Flows.

## The Mapping record

`knowledge-base/mapping-record.md` is the working document of the mapping: it describes the mapping, where every other file of `knowledge-base/` describes the app. It is the only state of the mapping besides the knowledge base itself, so every session leaves it true before it ends. It is deleted once the app is mapped.

```markdown
# Mapping record

Inventory taken at commit `4f1c2ab9…` (full id): 22 pages, 129 endpoints, 3 scheduled jobs, 2 incoming events.
Pilot: not run

## Areas

| Area | Is | Flows, roughly | Such as | State |
|---|---|---|---|---|
| Chat | Talking to an agent in a thread. | 8 | Start a thread; Approve a tool call | in progress |
| Agents | Setting up an agent and its tools. | 6 | Create an agent; Add a server to an agent | not gone into |

## Entry points

| Kind | Entry point | In | Area | Belongs to |
|---|---|---|---|---|
| page | /agents/[id]/chat | web/src/app/agents/[id]/chat/page.tsx | Chat | Flow: start-a-thread |
| endpoint | POST /threads/{id}/runs | backend/app/runs/router.py | Chat | Flow: start-a-thread, Flow to write: stop-a-run |
| job | Trigger scheduler, every minute | backend/app/triggers/scheduler.py | Triggers | not looked at yet |
| endpoint | GET /health | backend/app/main.py | | no Flow: the host's uptime probe, no Actor observes it |
```

- **Pilot** is `not run`, `waiting for the Builder` or `passed`.
- An Area's **State** is `not gone into`, `list to correct` (its Flows are listed and the Builder has not corrected the list yet), `in progress` or `done`.
- **Entry point** names it as someone outside the system meets it: the address of a page, the method and path of an endpoint, the name and rhythm of a job, the event and where it comes from. **In** is the file that declares it. This is the one file of `knowledge-base/` where a code path is written outside an Anchor.
- **Belongs to** is one of four things: `Flow: <id>` for a Flow that has a file, `Flow to write: <id>` for an entry of `flows_to_write`, `not looked at yet`, or `no Flow: <reason>`. An Entry point that serves several Flows lists each.
- An Area is a row here, and only here, until its first Flow or Flow to write: only then does it enter `areas.yaml`. Until then, renaming it, changing what it covers or dropping it changes this file and nothing else.

Bring the record back in line with the knowledge base whenever you read it: a row that says `Flow to write: <id>` for a Flow that now has a file becomes `Flow: <id>`, and an Area's State follows its rows.
